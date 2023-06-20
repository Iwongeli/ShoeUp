import pandas as pd
from website_scrapers._base import BaseScraper
import requests


class StockX(BaseScraper):
    url = "https://stockx.com/api/browse"
    brands = [
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
    important_cols = [
        "brand",
        "shoe",
        "styleId",
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

    def __init__(self) -> None:
        self.dfs = []

    def parse(self, response: requests.Response) -> pd.DataFrame:
        data = {}

        products = response.json()["Products"]

        for product in products:
            for key, value in product["market"].items():
                if key not in data:
                    data[key] = []
                data[key].append(value)

        for product in products:
            if product["market"]:
                product.pop("market")

            for key, value in product.items():
                if key not in data:
                    data[key] = []
                data[key].append(value)

        max_length = max(len(lst) for lst in data.values())
        for key in data:
            data[key] += [None] * (max_length - len(data[key]))

        df = pd.DataFrame(data)
        df = df.dropna(subset=["styleId"]).drop_duplicates("styleId")

        return df[self.important_cols]

    def run(self) -> pd.DataFrame:
        for brand in self.brands:
            params = {"resultsPerPage": 1000, "_search": brand}

            df = self.parse(self._get(params=params))
            self.dfs.append(df)

        return pd.concat(self.dfs)
