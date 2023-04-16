import sys
import time

from pathlib import Path
from datetime import datetime
import pandas as pd
import requests

from helper.general_helper import nft_meta_dict


def get_price(item):
    price = str(float(item) / 1000000000000000000)[:6]
    return price


class GemScraperListingPrice:
    def __init__(
            self,
            collection_slug,
            print_switch=False,
            n_item_per_scroll=10500,
            approx_max_n=50000,
    ):
        """
        :param collection_slug: the collection/asset slug shown in the collection of gem.xyz
        :param n_item_per_scroll: number of NFT items to be shown in each iteration (i.e., each scroll when temporary end of page is reached)
        :param approx_max_n: maximum number of NFT items to be scraped. Note, the end resulting maximum will be a multiple of n_item_per_scroll
        """
        assert approx_max_n >= n_item_per_scroll
        # Control panel
        self.print_switch = print_switch
        # Placeholder
        self.df = None
        # Params
        self.n_item_per_scroll = n_item_per_scroll
        self.approx_max_n = approx_max_n
        self.url = "https://api-v2-1.gemlabs.xyz/assets"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
            "x-api-key": "rLnNH1tdrT09EQjGsjrSS7V3uGonfZLW",
            "Origin": "https://www.gem.xyz",
        }

        self.params = {
            "filters": {
                "traits": {},
                "traitsRange": {},
                "slug": collection_slug,
                "rankRange": {},
                "price": {},
            },
            "sort": {"currentEthPrice": "asc"},
            "fields": {
                "id": 1,
                "name": 1,
                "address": 1,
                "collectionName": 1,
                "collectionSymbol": 1,
                "externalLink": 1,
                "imageUrl": 1,
                "smallImageUrl": 1,
                "animationUrl": 1,
                "openRarityRank": 1,
                "standard": 1,
                "perItemEthPrice": 1,
                "market": 1,
                "pendingTrxs": 1,
                "currentBasePrice": 1,
                "paymentToken": 1,
                "marketUrl": 1,
                "marketplace": 1,
                "tokenId": 1,
                "priceInfo": 1,
                "tokenReserves": 1,
                "ethReserves": 1,
                "sudoPoolAddress": 1,
                "sellOrders": 1,
                "startingPrice": 1,
                "rarityScore": 1,
            },
            "offset": 0,
            "limit": n_item_per_scroll,
            "markets": [],
            "status": ["buy_now"],
        }

    def scrape_gem_collection_infinite_scroll(self, print_switch=False):
        with requests.Session() as s:
            s.headers.update(self.headers)
            counter = 0
            output_list = []
            curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            while True:
                # response request statement
                try:
                    res = s.post(self.url, json=self.params)
                except:
                    continue

                for _ in range(
                        0, 20
                ):  # this for loop allows for n tries if it fails to crawl
                    try:
                        for item in res.json()["data"]:
                            item["scrapedTime"] = curr_time
                            output_list.append(item)

                            if print_switch:
                                item_id = item["id"]
                                item_name = item["name"]
                                item_price = float(
                                    get_price(item["priceInfo"]["price"])
                                )
                                item_sale_url = item["marketUrl"]
                                item_rarity_score = item["rarityScore"]

                                print("/////")
                                print(
                                    (
                                        curr_time,
                                        item_id,
                                        item_name,
                                        item_price,
                                        item_sale_url,
                                        item_rarity_score,
                                    )
                                )
                                print(item)
                        break

                    except Exception as e:
                        print("Error in scraping listing price:", e)
                        print("Re-trying...")
                        time.sleep(60)
                        continue

                self.params["offset"] += self.n_item_per_scroll
                counter += self.n_item_per_scroll

                if counter >= self.approx_max_n:
                    if print_switch:
                        print("Total number of scraped items:", counter)
                    break

            return output_list


if __name__ == "__main__":
    # Test
    curr_slug = nft_meta_dict["cryptopunksv1"]["gem_slug"]
    test_obj = GemScraperListingPrice(
        collection_slug=curr_slug, n_item_per_scroll=100, approx_max_n=50000
    )
    result = test_obj.scrape_gem_collection_infinite_scroll(print_switch=False)

    for i in result:
        print(i)

    print(len(result))
