import sys
import time
import datetime
from pathlib import Path

import pandas as pd
import numpy as np
from numpy.random import default_rng

from toolbox.web_scraper.scrape_gem_asset_listing_price import GemScraperListingPrice
from helper.general_helper import nft_meta_dict, control_panel


def path_to_output_file(collection_label):
    output_file_path = (
        Path(__file__).parent
        / "data/asset_listing_price"
        / collection_label
        / f"{collection_label}_asset_listing_price.csv"
    )
    return output_file_path


def periodically_save_asset_listing_price(
    selected_collection_key, n_item_per_scroll, approx_max_n, print_switch=False
):
    # Pull the list of saved assets in the collection so it doesn't repeat
    output_path = path_to_output_file(selected_collection_key)
    output_path.parent.mkdir(exist_ok=True)

    # Data structure
    data = {
        "_id": [],
        "collectionName": [],
        "tokenId": [],
        "url": [],
        "scrapedTime": [],
        "price": [],
    }

    while True:
        curr_collection_slug = nft_meta_dict[selected_collection_key]["gem_slug"]
        crawler = GemScraperListingPrice(
            collection_slug=curr_collection_slug,
            n_item_per_scroll=n_item_per_scroll,
            approx_max_n=approx_max_n,
        )

        if print_switch:
            print(
                f"Timestamp in scraping listed assets in {selected_collection_key}: {datetime.datetime.now()}"
            )

        result = crawler.scrape_gem_collection_infinite_scroll()

        # Arrange data
        for listed_item in result:
            data["_id"].append(listed_item["_id"])
            data["scrapedTime"].append(listed_item["scrapedTime"])
            data["collectionName"].append(listed_item["collectionName"])
            data["tokenId"].append(listed_item["tokenId"])
            data["url"].append(listed_item["url"])
            data["price"].append(
                round(
                    float(listed_item["priceInfo"]["pricePerItem"])
                    / (
                        10 ** int(listed_item["priceInfo"]["decimals"])
                        / int(listed_item["priceInfo"]["quantity"])
                    ),
                    6,
                )
            )

        # Saving data
        df = pd.DataFrame(data)
        if print_switch:
            print("DataFrame:", df.head())

        # Saving/appending
        with open(output_path, "a", newline="") as f:
            # Create file unless exists, otherwise append
            # Add header if file is being created, otherwise skip it
            df.to_csv(f, header=f.tell() == 0, index=False)

        # De-duplicaing, sorting
        df = pd.read_csv(output_path, sep=",", encoding="utf-8")
        df.drop_duplicates(subset=["scrapedTime", "tokenId"], keep="last", inplace=True)
        df = df.sort_values(by=["scrapedTime", "tokenId"], ascending=True)

        # Keep only the most recent 500,000 rows (otherwise, the g-drive sync is too slow, may need database
        # implementation later on if wanting to store more than 500,000 rows)
        if len(df) > 700500:
            df = df.iloc[-700000:]

        # Re-saving
        with open(output_path, "w", newline="") as f:
            df.to_csv(f, header=f.tell() == 0, index=False)

        # Reset `data`
        data = {
            "_id": [],
            "collectionName": [],
            "tokenId": [],
            "url": [],
            "scrapedTime": [],
            "price": [],
        }

        # Wait in between each scrape cycle
        # Add randomness to `wait_time`
        rng = default_rng()
        wait_time = control_panel["scrape_every_x_min"]
        wait_time = rng.uniform(wait_time * 0.999, wait_time * 1.001)
        time.sleep(wait_time)


if __name__ == "__main__":
    # collection_label: 'bayc', 'mayc', 'cryptopunksv1', 'cryptophunks', 'pridepunks', 'cryptoarte', 'mooncats', 'nftworlds'
    periodically_save_asset_listing_price(
        selected_collection_key="cryptopunksv1",
        n_item_per_scroll=200,
        approx_max_n=10000,
        print_switch=True,
    )
    
