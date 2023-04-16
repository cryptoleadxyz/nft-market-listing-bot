import sys
import time
import requests
from pprint import pprint
from helper.general_helper import nft_meta_dict


def single_item_payload(contract_address, token_id):
    payload = {
        "fields": {
            "address": 1,
            "animationUrl": 1,
            "collectionName": 1,
            "collectionSymbol": 1,
            "creator": 1,
            "currentBasePrice": 1,
            "decimals": 1,
            "description": 1,
            "ethReserves": 1,
            "externalLink": 1,
            "id": 1,
            "imageUrl": 1,
            "lastSale": 1,
            "market": 1,
            "marketplace": 1,
            "marketUrl": 1,
            "name": 1,
            "openRarityRank": 1,
            "owner": 1,
            "paymentToken": 1,
            "pendingTrxs": 1,
            "perItemEthPrice": 1,
            "priceInfo": 1,
            "rarityScore": 1,
            "sellOrders": 1,
            "smallImageUrl": 1,
            "standard": 1,
            "sudoPoolAddress": 1,
            "tokenId": 1,
            "tokenReserves": 1,
            "traits": 1,
        },
        "filters": {
            "address": contract_address,
            "tokenIds": [str(token_id)],
        },
        "limit": 1,
        "offset": 0,
        "refreshMetadata": False,
        "status": ["all"],
    }
    return payload


class GemScraperItemDetail:
    def __init__(self, collection_contract):
        """
        :param collection_contract: the smart contract address of the nft collection
        """
        # Control panel
        # Placeholder
        self.df = None
        # Params
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-api-key': 'rLnNH1tdrT09EQjGsjrSS7V3uGonfZLW',
            'Origin': 'https://www.gem.xyz'
        }
        self.collection_contract = collection_contract
        self.base_url = 'https://api-v2-1.gemlabs.xyz/assets'

    def scrape_single_asset_static_info_from_gem(self, token_id):
        with requests.Session() as s:
            s.headers.update(self.headers)
            curr_payload = single_item_payload(
                self.collection_contract, token_id)

            counter = 0
            while True:
                try:
                    item_info = s.post(
                        self.base_url, headers=self.headers, json=curr_payload).json()
                    return item_info

                except:
                    counter += 1
                    print(
                        'Failed to scrape data, prolonged waiting before re-attempt, counter:', counter)
                    time.sleep(60*12)  # wait xx min when denied access
                    if counter > 30:
                        print('Too many failed attempts, exit program...')
                        break
                    else:
                        continue


if __name__ == '__main__':
    # Test
    curr_contract = nft_meta_dict['cryptopunksv1']['contract']
    test_obj = GemScraperItemDetail(collection_contract=curr_contract)
    test_result = test_obj.scrape_single_asset_info_from_gem(token_id=1279)
    print(test_result)
