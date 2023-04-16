import os
import sys
import getopt
import time
import warnings
from pathlib import Path
import datetime
from datetime import timedelta
from dotenv import load_dotenv

from numpy.random import default_rng
import pandas as pd

from helper.general_helper import (
    nft_meta_dict,
    other_discord_channel,
    pandas_output_setting,
    asset_filter_dict,
    control_panel,
)
from nextcord import Intents
from nextcord.ext import commands

# Control panel
warnings.filterwarnings("ignore")
debug_switch = True
full_df_output_display_switch = True
load_dotenv()
my_discord_bot_token = os.getenv("DISCORD_TOKEN")
relative_price_diff_threshold = 0.03
n_day_lookup = 3
price_decimal = 3


async def send_message_to_discord_channel(discord_bot, discord_channel, message):
    channel = discord_bot.get_channel(discord_channel)
    output_message_split = message.split(" |||")
    for new_line in output_message_split:
        if new_line:
            for i in range(10):  # retry x number of times
                try:
                    await channel.send(new_line)
                    # time.sleep(0.1)
                    break
                except Exception as e:
                    print(
                        f"Error: Unable to send message to discord channel, re-try attempt #{i+1}"
                    )


def run_discord_bot(discord_bot_token, nft_collection_key):
    # Discord bot control
    intents = Intents.default()
    intents.message_content = True
    discord_bot = commands.Bot(command_prefix="!", intents=intents)

    def convert_snake_to_camelcase(my_string):
        my_string = str(my_string)
        return "".join(x.capitalize() or "_" for x in my_string.split("_"))

    def path_to_saved_asset_listing_price_file(collection_label):
        output_file_path = (
            Path(__file__).parent
            / "data/asset_listing_price"
            / collection_label
            / f"{collection_label}_asset_listing_price.csv"
        )
        return output_file_path

    def path_to_saved_asset_static_info_file(collection_label):
        output_file_path = (
            Path(__file__).parent
            / "data/asset_static_info"
            / collection_label
            / f"{collection_label}_asset_static_info.csv"
        )
        return output_file_path

    def extract_unique_token_id_from_tuple_lists(list_current, list_previous):
        output_list = []
        for token_id_current, price_current in list_current:
            for token_id_previous, price_previous in list_previous:
                if token_id_current == token_id_previous:
                    if (
                        abs((price_current - price_previous) / price_previous)
                        > relative_price_diff_threshold
                    ):
                        output_list.append(token_id_current)
        return output_list

    def apply_asset_filter(
        row, selected_collection_key, asset_filter_dict, global_floor_price
    ):
        output = []
        # Include collection-specific criteria AND generic criteria that apply to all collections
        asset_filter = (
            asset_filter_dict[selected_collection_key] + asset_filter_dict["_generic"]
        )

        for criterion in asset_filter:

            if debug_switch:
                print(criterion)

            # this has to be specified
            assert (
                (criterion["tier"] == 1)
                | (criterion["tier"] == 2)
            )
            assert (
                criterion["token_id_any"] is not None
            )  # this can either be empty [] or populated list
            assert (
                criterion["trait_string_any"] is not None
            )  # this can either be empty [] or populated list
            assert (
                criterion["trait_string_all"] is not None
            )  # this can either be empty [] or populated list
            assert (
                criterion["trait_string_not"] is not None
            )  # this can either be empty [] or populated list
            fulfill_count = 0
            success_fulfill_count = (
                len(criterion) - 1
            )  # subtract 1 since `tier` isn't a filter requirement
            filter_label = ""

            if len(criterion["trait_string_any"]) > 0:
                adding_trait_count_any = 0
                for trait in criterion["trait_string_any"]:
                    if trait in str(row["traits"]):
                        adding_trait_count_any += 1
                if adding_trait_count_any >= 1:
                    fulfill_count += 1
                    filter_label = f"_{convert_snake_to_camelcase('trait_string_any')}=({convert_snake_to_camelcase(criterion['trait_string_any'])})"
            else:
                fulfill_count += 1

            if len(criterion["trait_string_all"]) > 0:
                adding_trait_count_all = 0
                success_trait_count_all = len(criterion["trait_string_all"])
                for trait in criterion["trait_string_all"]:
                    if trait in str(row["traits"]):
                        adding_trait_count_all += 1
                if adding_trait_count_all == success_trait_count_all:
                    fulfill_count += 1
                    filter_label = f"_{convert_snake_to_camelcase('trait_string_all')}=({convert_snake_to_camelcase(criterion['trait_string_all'])})"
            else:
                fulfill_count += 1

            if len(criterion["trait_string_not"]) > 0:
                adding_trait_count_all = 0
                success_trait_count_all = 0
                for trait in criterion["trait_string_not"]:
                    if trait in str(row["traits"]):
                        adding_trait_count_all += 1
                if adding_trait_count_all == success_trait_count_all:
                    fulfill_count += 1
                    filter_label = f"_{convert_snake_to_camelcase('trait_string_not')}=({convert_snake_to_camelcase(criterion['trait_string_not'])})"
            else:
                fulfill_count += 1

            if criterion["min_rank"] is not None:
                if criterion["min_rank"] >= row["rarityScore"]:
                    fulfill_count += 1
                    filter_label = (
                        filter_label
                        + f"_{convert_snake_to_camelcase('min_rank')}={convert_snake_to_camelcase(criterion['min_rank'])}"
                    )
            else:
                fulfill_count += 1

            if criterion["max_abs_price"] is not None:
                if criterion["max_abs_price"] >= row["price"]:
                    fulfill_count += 1
                    filter_label = (
                        filter_label
                        + f"_{convert_snake_to_camelcase('max_abs_price')}={convert_snake_to_camelcase(criterion['max_abs_price'])}"
                    )
            else:
                fulfill_count += 1

            if criterion["max_rel_flr_price_multiplier"] is not None:
                if (
                    criterion["max_rel_flr_price_multiplier"] * global_floor_price
                    >= row["price"]
                ):
                    fulfill_count += 1
                    filter_label = (
                        filter_label
                        + f"_{convert_snake_to_camelcase('max_rel_flr_price_multiplier')}={convert_snake_to_camelcase(criterion['max_rel_flr_price_multiplier'])}"
                    )
            else:
                fulfill_count += 1

            if len(criterion["token_id_any"]) > 0:
                if row["tokenId"] in criterion["token_id_any"]:
                    fulfill_count += 1
                    filter_label = (
                        filter_label
                        + f"_{convert_snake_to_camelcase('token_id_any')}={convert_snake_to_camelcase(criterion['token_id_any'])}"
                    )
            else:
                fulfill_count += 1

            if fulfill_count == success_fulfill_count:
                filter_label = f"<<Tier{criterion['tier']}_{filter_label}>>"
                filter_label = filter_label.replace("__", "_")
                filter_label = filter_label.replace("_>>", ">>")
                output.append(filter_label)

            if debug_switch:
                print(filter_label)

        if debug_switch:
            print(output)

        return output

    async def periodically_monitor_and_alert_asset_with_potential(
        selected_collection_key,
        n_day_lookup=n_day_lookup,
        price_decimal=price_decimal,
        discord_alert_switch=True,
        print_switch=False,
    ):
        if full_df_output_display_switch:
            pandas_output_setting()

        price_data_path = path_to_saved_asset_listing_price_file(
            selected_collection_key
        )
        info_data_path = path_to_saved_asset_static_info_file(selected_collection_key)

        iter_loop_n = 0
        listing_price_data_checker = []

        while True:
            if print_switch:
                print("\n////////////////////////////////////////" * 2)
                print(
                    f"Scanning #{iter_loop_n}: {selected_collection_key.upper()} at {datetime.datetime.now()}..."
                )

            iter_loop_n += 1

            # try 10 times if program can't access `price_data_path` file; wait 60 sec in between
            for i in range(0, 10):
                try:
                    df_price = pd.read_csv(price_data_path, sep=",", encoding="utf-8")
                    break
                except:
                    if print_switch:
                        print("Error: Failed reading `df_price` data, re-trying...")
                    time.sleep(60)
                    continue

            df_info = pd.read_csv(info_data_path, sep=",", encoding="utf-8")[
                ["tokenId", "traits", "rarityScore"]
            ]

            # Time and price column standardization
            df_price["scrapedTime"] = pd.to_datetime(df_price["scrapedTime"])
            df_price.sort_values(by="scrapedTime", ascending=True, inplace=True)
            df_price["price"] = df_price["price"].round(decimals=price_decimal)
            # Remove rows with missing data
            df_price = df_price.dropna(subset=["price", "scrapedTime"])
            assert df_price["price"].isna().sum() == 0
            assert df_price["scrapedTime"].isna().sum() == 0

            # Execute the logics of finding new listings
            # Get the lastest timestamp (i.e., each succession of timestamp is ~10m) and use it to splice the `df_price`
            latest_timestamp = df_price["scrapedTime"].max()
            df_price_current = df_price[df_price["scrapedTime"] == latest_timestamp]
            df_price_current.drop_duplicates(
                subset=["tokenId", "price"], keep="last", inplace=True
            )
            df_price_current["tokenId"] = df_price_current["tokenId"].astype("int")

            # Check if the listing price database is updated - if `latest_timestamp` in this loop is the same as `latest_timestamp`
            # the one multiple loops before, that means the listing price data is not adding new rows
            listing_price_data_checker.append(latest_timestamp)
            if len(listing_price_data_checker) > 5:
                assert latest_timestamp != listing_price_data_checker[0]
                listing_price_data_checker = listing_price_data_checker[-5:]

            # New listing definition logic
            # Pseudo code:
            #   create df_current and df_price_previous_agg
            #       1) any tokenId in df_current but not in df_price_previous_agg -> new listings
            #       2) any tokenId in both df_current and df_price_previous_agg, and if the current price is different than last previous -> considered new listings
            #       3) any tokenId in both df_current and df_price_previous_agg, and if the current price is the same than last previous -> considered old listings
            # Only using last x listings as historical comparison to define "new listing"
            # Can't use last (or current) day because it's still being scraped
            df_price_yesterday = df_price.copy()
            df_price_yesterday["scrapedTime"] = pd.to_datetime(
                df_price_yesterday["scrapedTime"]
            )
            df_price_yesterday.sort_values(
                by="scrapedTime", ascending=True, inplace=True
            )
            df_price_yesterday["scrapedDate"] = df_price_yesterday[
                "scrapedTime"
            ].dt.date

            second_last_day = df_price_yesterday["scrapedDate"].max()
            second_last_day = df_price_yesterday["scrapedDate"].max() - timedelta(
                days=1
            )
            df_price_yesterday = df_price_yesterday[
                df_price_yesterday["scrapedDate"] == second_last_day
            ]
            n_row_on_second_last_day = len(df_price_yesterday)
            if n_row_on_second_last_day == 0:  # placeholder
                n_row_on_second_last_day == 100000
            # Cut out the last date; then cut data based on the approximated number of rows in a pre-defined day range
            df_price_previous = df_price[df_price["scrapedTime"] != latest_timestamp][
                -2 * (n_day_lookup) * (n_row_on_second_last_day) :
            ]
            df_price_previous["tokenId"] = df_price_previous["tokenId"].astype("int")
            print(
                f'Logging: second last day as "{second_last_day}", latest timestamp as "{latest_timestamp}"...'
            )

            # Create second latest df so I can get a recent global floor price, but not including all prevoius values (otherwise it will be irrelevant if using super old data)
            second_latest_timestamp = df_price_previous["scrapedTime"].max()
            df_price_previous_latest = df_price_previous[
                df_price_previous["scrapedTime"] == second_latest_timestamp
            ]
            previous_latest_global_floor_price = df_price_previous_latest["price"].min()

            # Newly listed asset list #1; completely new list
            current_token_id_list_1a = df_price_current["tokenId"].tolist()
            previous_token_id_list_1a = df_price_previous["tokenId"].tolist()
            newly_listed_1a = list(
                set(current_token_id_list_1a) - set(previous_token_id_list_1a)
            )
            if debug_switch:
                print("newly_listed_1a:", newly_listed_1a)

            # Newly listed asset list #2; changed price should also be considered as new listing
            # Create a `newly_listed` that contains only new assets' `name` and `price`
            df_price_current_agg = (
                df_price_current.copy().groupby(["tokenId"], as_index=False).last()
            )
            df_price_current_agg["combined"] = df_price_current_agg[
                ["tokenId", "price"]
            ].apply(tuple, axis=1)
            df_price_previous_agg = (
                df_price_previous.copy().groupby(["tokenId"], as_index=False).last()
            )
            df_price_previous_agg["combined"] = df_price_previous_agg[
                ["tokenId", "price"]
            ].apply(tuple, axis=1)

            current_token_id_list_1b = df_price_current_agg["combined"].tolist()
            previous_token_id_list_1b = df_price_previous_agg["combined"].tolist()
            newly_listed_1b = extract_unique_token_id_from_tuple_lists(
                list_current=current_token_id_list_1b,
                list_previous=previous_token_id_list_1b,
            )
            if debug_switch:
                print("newly_listed_1b:", newly_listed_1b)

            # Combine "Newly listed asset list #1" and "Newly listed asset list #2"
            newly_listed_combined = list(set(newly_listed_1a) | set(newly_listed_1b))
            # Ensure the list values are all integers
            newly_listed_1a = [int(token_id) for token_id in newly_listed_1a]
            newly_listed_1b = [int(token_id) for token_id in newly_listed_1b]
            newly_listed_combined = [
                int(token_id) for token_id in newly_listed_combined
            ]

            if debug_switch:
                print("newly_listed_combined:", newly_listed_combined)
            # Get a trimmed df that only has newly listed assets
            df_newly_listed = df_price_current[
                df_price_current["tokenId"].isin(newly_listed_combined)
            ]
            # Merge with trait and rank data
            df_newly_listed = df_newly_listed.merge(df_info, on="tokenId", how="left")

            # Apply asset filter
            asset_filter = asset_filter_dict[selected_collection_key]
            assert asset_filter is not None

            # Find global floor price just 1 time slice prior to `df_price_current`
            # so that it doesn't include all historical value (too low), and still be able to show new listing that significantly below previous floor
            # this is for output with any tier (or all tiers)
            output_message = ""
            output_message_filtered = ""

            # If no listing, can print out in terminal, but no need to send to discord
            if len(df_newly_listed) == 0:
                if print_switch:
                    print("\nNo new listing...")

            elif len(df_newly_listed) > 0:
                output_message += "\n////////////////////////////////////////"
                output_message += f'\nGlobal floor price for "{selected_collection_key.upper()}" from most recent time snapshot ({datetime.datetime.now()}): {previous_latest_global_floor_price}'
                output_message_filtered += "\n////////////////////////////////////////"
                output_message_filtered += f'\nGlobal floor price for "{selected_collection_key.upper()}" from most recent time snapshot ({datetime.datetime.now()}): {previous_latest_global_floor_price}'

                df_newly_listed["filter"] = df_newly_listed.apply(
                    apply_asset_filter,
                    args=(
                        selected_collection_key,
                        asset_filter_dict,
                        previous_latest_global_floor_price,
                    ),
                    axis=1,
                )
                output_message += "\n........................................."
                output_message += f"\nAll new listing(s), n: {len(df_newly_listed)}"

                for i in range(len(df_newly_listed)):
                    try:
                        rarity_output = str(int(df_newly_listed.loc[i, "rarityScore"]))
                    except:
                        rarity_output = "N/A"

                    output_message += f"\n>> {nft_collection_key.upper()}/ TokenId: {df_newly_listed.loc[i, 'tokenId']}/ Price: {df_newly_listed.loc[i, 'price']}/ Rarity: {rarity_output}/"
                    """
                    if df_newly_listed.loc[i, "filter"] != []:
                        output_message += (
                            f"\nFilter: {df_newly_listed.loc[i, 'filter']}"
                        )
                    """
                    output_message += f"\n{df_newly_listed.loc[i, 'url']}"
                    output_message += " |||"

                # Send alert when there is signal from "filter" column
                df_newly_listed_filtered = df_newly_listed[
                    df_newly_listed["filter"].apply(len).gt(0)
                ]
                df_newly_listed_filtered = df_newly_listed_filtered.reset_index()

                if len(df_newly_listed_filtered) > 0:
                    output_message_filtered += (
                        "\n........................................."
                    )
                    output_message_filtered += f"\nNew listing(s) with predefined filter signals, n: {len(df_newly_listed_filtered)}"

                    for i in range(len(df_newly_listed_filtered)):
                        try:
                            rarity_output = str(
                                int(df_newly_listed_filtered.loc[i, "rarityScore"])
                            )
                        except:
                            rarity_output = "N/A"

                        output_message_filtered += f"\n>> {nft_collection_key.upper()}/ TokenId: {df_newly_listed_filtered.loc[i, 'tokenId']}/ Price: {df_newly_listed_filtered.loc[i, 'price']}/ Rarity: {rarity_output}"

                        if df_newly_listed_filtered.loc[i, "filter"] != []:
                            output_message_filtered += (
                                f"\nFilter: {df_newly_listed_filtered.loc[i, 'filter']}"
                            )
                        output_message_filtered += (
                            f"\n{df_newly_listed_filtered.loc[i, 'url']}"
                        )
                        output_message_filtered += " |||"

                # Send message to discord channels
                if debug_switch:
                    print("Non-filtered message")
                    print(output_message_filtered)
                    print("/////")
                    print("Filtered message")
                    print(output_message_filtered)

                if discord_alert_switch:
                    if "tier1" in output_message_filtered.lower():
                        if debug_switch:
                            print("Tier1 signal triggered")

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_tier1"
                            ],
                            message= output_message_filtered,
                        )

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_tier2"
                            ],
                            message= output_message_filtered,
                        )

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_all_tier"
                            ],
                            message=output_message,
                        )

                    elif "tier2" in output_message_filtered.lower():
                        if debug_switch:
                            print("Tier2 signal triggered")

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_tier2"
                            ],
                            message= output_message_filtered,
                        )

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_all_tier"
                            ],
                            message=output_message,
                        )

                    else:
                        if debug_switch:
                            print("Neither Tier1 nor Tier2 signal triggered")

                        await send_message_to_discord_channel(
                            discord_bot=discord_bot,
                            discord_channel=nft_meta_dict[selected_collection_key][
                                "discord_channel_listing_all_tier"
                            ],
                            message=output_message,
                        )

            if print_switch:
                print('Text of output_message')
                print(output_message)

            # Wait time between each monitoring cycle
            # Add randomness to `wait_time`
            rng = default_rng()
            wait_time = (
                control_panel["scrape_every_x_min"] * 0.999
            )  # make sure it's slightly less than the price crawling cycle to ensure the new data must be monitored at least 1
            # wait_time = rng.uniform(wait_time * 0.999, wait_time * 1.001)
            time.sleep(wait_time)

    @discord_bot.event
    async def on_ready():
        # collection_label: 'bayc', 'cryptopunksv1', 'cryptoarte', 'mooncats', 'nftworlds', 'cryptophunks'
        await periodically_monitor_and_alert_asset_with_potential(
            selected_collection_key=nft_collection_key,
            n_day_lookup=n_day_lookup,
            price_decimal=price_decimal,
            discord_alert_switch=True,
            print_switch=True,
        )

    for _ in range(0, 30):
        try:
            discord_bot.run(discord_bot_token)
        except Exception as e:
            print(e)
            print("Error: Discord bot can not connect to discord, re-trying...")
            time.sleep(60)


if __name__ == "__main__":
    command_line_switch = False

    if command_line_switch:
        # Remove 1st argument from the
        # List of command line arguments
        argumentList = sys.argv[1:]
        # Options
        options = "hmn:"
        # Long options
        long_options = ["help", "my_file", "nft_collection_key"]

        try:
            # Parsing argument
            arguments, values = getopt.getopt(argumentList, options, long_options)

            # Checking each argument
            for currentArgument, currentValue in arguments:

                if currentArgument in ("-h", "--help"):
                    print("Displaying help (TBD)")

                elif currentArgument in ("-m", "--my_file"):
                    print("Displaying file_name:", sys.argv[0])

                elif currentArgument in ("-n", "--nft_collection_key"):
                    print(f"Executing main() for {currentValue.capitalize()}")
                    run_discord_bot(
                        discord_bot_token=my_discord_bot_token,
                        nft_collection_key=currentValue,
                    )

        except getopt.error as err:
            # Output error, and return with an error code
            print(str(err))

    else:
        # collection_label: 'bayc', 'mayc', 'cryptopunksv1', 'cryptophunks', 'pridepunks', 'cryptoarte', 'mooncats', 'nftworlds'
        run_discord_bot(
            discord_bot_token=my_discord_bot_token,
            nft_collection_key="nftworlds",
        )
