import logging
import multiprocessing.managers

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class Eobuwie(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.url = "https://eobuwie.com.pl/t-api/rest/search/eobuwie/v4/search"
        self.dfs = []
        self.categories = ("meskie", "damskie")
        self.params = {
            "channel": "eobuwie",
            "currency": "PLN",
            "locale": "pl_PL",
            "limit": 48,
            "page": 1,
            "categories[]": "meskie",
            "select[]": ["model", "final_price", "url_key"],
            "filters[marka][in][]": [
                "adidas",
                "adidas_originals",
                "adidas_performance",
                "adidas_sportswear",
                "converse",
                "jordan",
                "new_balance",
                "nike",
                "puma",
                "reebok",
                "reebok_classic",
                "vans",
                "asics",
            ],
        }

    def run(
        self, manager_dict: multiprocessing.managers.DictProxy = None
    ) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        for category in self.categories:
            self.params["categories[]"] = category
            while True:
                df = self.parse(self._get(params=self.params))

                if df.empty is False:
                    self.dfs.append(df)
                    self.params["page"] += 1
                else:
                    break

        df_concated = pd.concat(self.dfs)
        df_concated["shop"] = self.__class__.__name__

        if manager_dict is not None:
            manager_dict[self.__class__.__name__] = df_concated

        return df_concated

    def parse(self, response: requests.Response) -> pd.DataFrame:
        def parse_model(value):
            model_list = value.split()
            if len(model_list[-1]) < 5 and len(model_list) > 2:
                return model_list[-2] + "-" + model_list[-1]
            else:
                return model_list[-1]

        products = response.json()["products"]

        if len(products) <= 0:
            return pd.DataFrame()

        data = {"id": [], "price": [], "link": []}

        for product in products:
            data["id"].append(parse_model(product["values"]["model"]["value"]))
            data["price"].append(
                product["values"]["final_price"]["value"]["pl_PL"]["PLN"]["amount"]
            )
            data["link"].append(
                "https://eobuwie.com.pl/p/"
                + product["values"]["url_key"]["value"]["pl_PL"]
            )

        return pd.DataFrame(data)
