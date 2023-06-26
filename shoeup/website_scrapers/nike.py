import logging

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class NikeScraper(BaseScraper):
    url = "https://api.nike.com/cic/browse/v2"

    def __init__(self) -> None:
        self.dfs = []

    def parse(self, response: requests.Response) -> pd.DataFrame:
        data = {"id": [], "price": [], "link": []}

        products = response.json()["data"]["products"]["products"]

        if products:
            for product in products:
                if product["inStock"] and product["productType"] == "FOOTWEAR":
                    data["id"].append(product["url"].split("/")[-1])
                    data["price"].append(product["price"]["currentPrice"])
                    data["link"].append(
                        "https://www.nike.com/pl/" + product["url"][14:]
                    )
        else:
            return pd.DataFrame({})

        return pd.DataFrame(data)

    def run(self) -> pd.DataFrame:
        logging.info('Start scraping Nike')

        params = {
            "queryid": "products",
            "anonymousId": "60DE7E4BCCCD1D7470D10F44D33348F0",
            "country": "pl",
            "endpoint": "/product_feed/rollup_threads/v2?filter=marketplace(PL)&filter=language(pl)&filter=employeePrice(true)&filter=attributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c)&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24",
            "language": "pl",
            "localizedRangeStr": "{lowestPrice} – {highestPrice}",
        }
        anchor = 0

        while True:
            params[
                "endpoint"
            ] = f"/product_feed/rollup_threads/v2?filter=marketplace(PL)&filter=language(pl)&filter=employeePrice(true)&filter=attributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c)&anchor={anchor}&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24"

            df = self.parse(self._get(params=params))

            if df.empty is False:
                self.dfs.append(df)
                anchor += 24
            else:
                break

        return pd.concat(self.dfs)
