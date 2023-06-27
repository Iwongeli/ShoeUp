import logging

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class Adidas(BaseScraper):
    url = "https://www.adidas.pl/api/plp/content-engine"

    def __init__(self) -> None:
        self.dfs = []

        self.headers[
            "user-agent"
        ] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
        del self.headers["accept-language"]

    def parse(self, response: requests.Response) -> pd.DataFrame:
        data = {"id": [], "price": [], "link": []}

        products = response.json()["raw"]["itemList"]["items"]

        if len(products) > 0:
            for product in products:
                data["id"].append(product["modelId"])
                data["price"].append(product["salePrice"])
                data["link"].append("https://www.adidas.pl/" + product["link"])
        else:
            return pd.DataFrame({})

        return pd.DataFrame(data)

    def run(self) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        params = {
            "experiment": "CORP_BEN",
            "query": "mezczyzni-buty",
        }
        start = 0

        while True:
            params["start"] = start

            df = self.parse(self._get(params=params))

            if df.empty is False:
                self.dfs.append(df)
                start += 48
            else:
                break

        return pd.concat(self.dfs)