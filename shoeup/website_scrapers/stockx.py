import logging
import multiprocessing.managers

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class StockX(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.url = "https://stockx.com/api/browse"
        self.brands = [
            "adidas",
            "Nike",
            "Jordan",
            "New Balance",
            "Vans",
            "Reebok",
            "Converse",
            "Puma",
            "ASICS",
        ]
        self.important_cols = [
            "brand",
            "shoe",
            "styleId",
            "averageDeadstockPrice",
            "highestBid",
            "lowestAsk",
            "numberOfAsks",
            "salesThisPeriod",
            "salesLastPeriod",
            "numberOfBids",
            "deadstockRangeLow",
            "deadstockRangeHigh",
            "volatility",
            "deadstockSold",
            "lastSale",
            "salesLast72Hours",
            "deadstockSoldRank",
            "averageDeadstockPriceRank",
        ]
        self.dfs = []

    def parse(self, response: requests.Response) -> pd.DataFrame:
        data = {}

        products = response.json()["Products"]

        for product in products:
            product_items = product.pop("market", {})
            product_items.update(product)

            for key, value in product_items.items():
                data.setdefault(key, []).append(value)

        max_length = max(len(lst) for lst in data.values())
        for key in data:
            data[key] += [None] * (max_length - len(data[key]))

        df = pd.DataFrame(data)
        df = df.dropna(subset=["styleId"]).drop_duplicates("styleId")

        return df[self.important_cols]

    def run(
        self, manager_dict: multiprocessing.managers.DictProxy = None
    ) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        for brand in self.brands:
            logging.info("Start scraping brand %s", brand)

            params = {"resultsPerPage": 1000, "_search": brand}

            df = self.parse(self._get(params=params))
            self.dfs.append(df)

        df_concated = pd.concat(self.dfs)

        if manager_dict is not None:
            manager_dict[self.__class__.__name__] = df_concated

        return df_concated
