import logging
import multiprocessing.managers

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class Nike(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.url = "https://api.nike.com/cic/browse/v2"
        self.dfs = []
        self.params = {
            "queryid": "products",
            "anonymousId": "60DE7E4BCCCD1D7470D10F44D33348F0",
            "country": "pl",
            "endpoint": "/product_feed/rollup_threads/v2?filter=marketplace(PL)&filter=language(pl)&filter=employeePrice(true)&filter=attributeIds(0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c)&anchor=0&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24",
            "language": "pl",
            "localizedRangeStr": "{lowestPrice} – {highestPrice}",
        }
        self.attribute_ids = (
            "16633190-45e5-4830-a068-232ac7aea82c,7baf216c-acc6-4452-9e07-39c2ca77ba32",  # women shoes
            "0f64ecc7-d624-4e91-b171-b83a03dd8550,16633190-45e5-4830-a068-232ac7aea82c",  # men shoes
        )

    def parse(self, response: requests.Response) -> pd.DataFrame:
        data = {"id": [], "price": [], "link": []}

        products = response.json()["data"]["products"]["products"]

        if not products:
            return pd.DataFrame({})

        for product in products:
            if product["inStock"] and product["productType"] == "FOOTWEAR":
                data["id"].append(product["url"].split("/")[-1])
                data["price"].append(product["price"]["currentPrice"])
                data["link"].append("https://www.nike.com/pl/" + product["url"][14:])

        return pd.DataFrame(data)

    def run(
        self, manager_dict: multiprocessing.managers.DictProxy = None
    ) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        anchor = 0

        for id in self.attribute_ids:
            self.params[
                "endpoint"
            ] = f"/product_feed/rollup_threads/v2?filter=marketplace(PL)&filter=language(pl)&filter=employeePrice(true)&filter=attributeIds({id})&anchor={anchor}&consumerChannelId=d9a5bc42-4b9c-4976-858a-f159cf99c647&count=24"

            while True:
                df = self.parse(self._get(params=self.params))

                if df.empty is False:
                    self.dfs.append(df)
                    anchor += 24
                else:
                    break

        df_concated = pd.concat(self.dfs)
        df_concated["shop"] = self.__class__.__name__

        if manager_dict is not None:
            manager_dict[self.__class__.__name__] = df_concated

        return df_concated
