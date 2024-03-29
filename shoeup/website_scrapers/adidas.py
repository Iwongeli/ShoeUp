import logging
import multiprocessing.managers

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class Adidas(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.url = "https://www.adidas.pl/api/plp/content-engine"
        self.dfs = []
        self.headers[
            "user-agent"
        ] = "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
        del self.headers["accept-language"]
        self.queries = ("mezczyzni-buty", "kobiety-buty")
        self.params = {
            "experiment": "CORP_BEN",
            "query": "mezczyzni-buty",
        }
        self.start = 0

    def parse(self, response: requests.Response) -> pd.DataFrame:
        products = response.json()["raw"]["itemList"]["items"]

        if len(products) <= 0:
            return pd.DataFrame()

        data = {"id": [], "price": [], "link": []}

        for product in products:
            data["id"].append(product["modelId"])
            data["price"].append(product["salePrice"])
            data["link"].append("https://www.adidas.pl/" + product["link"])

        return pd.DataFrame(data)

    def run(
        self, manager_dict: multiprocessing.managers.DictProxy = None
    ) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        for query in self.queries:
            self.params["query"] = query
            while True:
                self.params["start"] = self.start

                df = self.parse(self._get(params=self.params))

                if df.empty is False:
                    self.dfs.append(df)
                    self.start += 48
                else:
                    break

        df_concated = pd.concat(self.dfs)
        df_concated["shop"] = self.__class__.__name__

        if manager_dict is not None:
            manager_dict[self.__class__.__name__] = df_concated

        return df_concated
