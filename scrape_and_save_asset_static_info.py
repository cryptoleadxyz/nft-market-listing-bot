import sys
import time
import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from numpy.random import default_rng

from toolbox.web_scraper.scrape_gem_asset_static_info import GemScraperItemDetail
from helper.general_helper import nft_meta_dict


def path_to_output_file(collection_label, scraped_time):
    '''
    `scraped_time`: in yyyy-mm-dd such as 2022-12-24
    '''
    output_file_path = (
        Path(__file__).parent
        / "data/asset_static_info"
        / collection_label
        / f"{collection_label}_asset_static_info_{scraped_time}.csv"
    )
    return output_file_path


def loop_and_save_asset_static_info(
    selected_collection_key,
    print_switch=False,
    start_scrape_n=0,
    end_scrape_n=10000,
    wait_time=20,
):
    # Pull the list of saved assets in the collection so it doesn't repeat
    scraped_date = datetime.datetime.today().strftime('%Y-%m-%d')
    output_path = path_to_output_file(selected_collection_key, scraped_date)
    output_path.parent.mkdir(exist_ok=True)

    try:
        with open(output_path, "r") as f:
            _ = pd.read_csv(f, header=0, engine="c")
            scraped_list = _["tokenId"].tolist()

    except:
        print("Unexpected error:", sys.exc_info()[0])
        scraped_list = []

    # Loop and store scraped info into df
    data = {
        "scrapedDate": [],
        "_id": [],
        "address": [],
        "collectionName": [],
        "collectionSymbol": [],
        "creator": [],
        "name": [],
        "tokenId": [],
        "traits": [],
        "rarityScore": [],
        "url": [],
        "lastSale": [],
    }

    curr_contract = nft_meta_dict[selected_collection_key]["contract"]
    crawler = GemScraperItemDetail(collection_contract=curr_contract)

    for i in range(start_scrape_n, end_scrape_n + 1):
        if i not in scraped_list:
            if print_switch:
                print(
                    f"Currently scraping item {i} in {selected_collection_key}...")

            if wait_time:
                # Add randomness to `wait_time`
                rng = default_rng()
                wait_time = rng.uniform(wait_time * 0.7, wait_time * 1.3)
                time.sleep(wait_time)

            result = crawler.scrape_single_asset_static_info_from_gem(token_id=i)

            if result["data"] != []:  # if 'data' is not an empty list
                data["scrapedDate"].append(scraped_date)
                data["_id"].append(result["data"][0]["_id"])

                if "address" in result["data"][0]:
                    data["address"].append(result["data"][0]["address"])
                else:
                    data["address"].append(np.nan)

                if "collectionName" in result["data"][0]:
                    data["collectionName"].append(
                        result["data"][0]["collectionName"])
                else:
                    data["collectionName"].append(np.nan)

                if "tokenId" in result["data"][0]:
                    data["tokenId"].append(result["data"][0]["tokenId"])
                else:
                    data["tokenId"].append(np.nan)

                if "traits" in result["data"][0]:
                    data["traits"].append(result["data"][0]["traits"])
                else:
                    data["traits"].append(np.nan)

                if "url" in result["data"][0]:
                    data["url"].append(result["data"][0]["url"])
                else:
                    data["url"].append(np.nan)

                if "lastSale" in result["data"][0]:
                    data["lastSale"].append(result["data"][0]["lastSale"])
                else:
                    data["lastSale"].append(np.nan)

                if "creator" in result["data"][0]:
                    data["creator"].append(result["data"][0]["creator"])
                else:
                    data["creator"].append(np.nan)

                if "name" in result["data"][0]:
                    data["name"].append(result["data"][0]["name"])
                else:
                    data["name"].append(np.nan)

                if "rarityScore" in result["data"][0]:
                    data["rarityScore"].append(
                        result["data"][0]["rarityScore"])
                else:
                    data["rarityScore"].append(9999999999)

                if "collectionSymbol" in result["data"][0]:
                    data["collectionSymbol"].append(
                        result["data"][0]["collectionSymbol"])
                else:
                    data["collectionSymbol"].append(np.nan)

                if print_switch:
                    if result["data"][0]["tokenId"] != i:
                        print("WARNING: token_id != i")

            else:
                data["scrapedDate"].append(scraped_date)
                data["_id"].append(np.nan)
                data["address"].append(np.nan)
                data["collectionName"].append(np.nan)
                data["collectionSymbol"].append(np.nan)
                data["creator"].append(np.nan)
                data["name"].append(np.nan)
                data["tokenId"].append(i)
                data["traits"].append(np.nan)
                data["rarityScore"].append(np.nan)
                data["url"].append(np.nan)
                data["lastSale"].append(np.nan)

            if print_switch:
                print("Iteration:", i)
                print(f"Timestamp: {datetime.datetime.now()}")
                print("Scraped result:", result)

            # Everytime i is divisible by xx, execute save, and refresh `data`
            if i % 10 == 0:
                # Set up dataframe and output path
                df = pd.DataFrame(data)
                if print_switch:
                    print("DataFrame:", df.head())

                # Saving/appending
                with open(output_path, "a", newline="", encoding="utf-8") as f:
                    # Create file unless exists, otherwise append
                    # Add header if file is being created, otherwise skip it
                    df.to_csv(f, header=f.tell() == 0, index=False)

                # De-duplicaing, sorting
                df = pd.read_csv(output_path, sep=",", encoding="utf-8")
                df.drop_duplicates(subset="tokenId", keep="last", inplace=True)
                df = df.sort_values(by="tokenId", ascending=False)

                # Re-saving
                with open(output_path, "w", newline="", encoding="utf-8") as f:
                    df.to_csv(f, header=f.tell() == 0, index=False)

                # Reset `data`
                data = {
                    "scrapedDate": [],
                    "_id": [],
                    "address": [],
                    "collectionName": [],
                    "collectionSymbol": [],
                    "creator": [],
                    "name": [],
                    "tokenId": [],
                    "traits": [],
                    "rarityScore": [],
                    "url": [],
                    "lastSale": [],
                }


if __name__ == "__main__":
    # collection_label: 'bayc', 'mayc', 'cryptopunksv1', 'cryptophunks', 'pridepunks', 'cryptoarte', 'mooncats', 'nftworlds'
    loop_and_save_asset_static_info(
        selected_collection_key="mooncats",
        print_switch=True,
        start_scrape_n=0,
        end_scrape_n=13000,  # for mooncats, do 25440; for 10K collections, do 10100; for mayc, do 13000
        wait_time=30,
    )
