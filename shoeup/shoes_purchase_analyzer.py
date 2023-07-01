import pandas as pd
import requests


class Analyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.usd_to_pln = self.get_usd_to_pln()

    @staticmethod
    def get_usd_to_pln() -> float:
        api = f"http://api.nbp.pl/api/exchangerates/rates/A/USD/"

        r = requests.get(api)
        r.raise_for_status()

        return float(r.json()["rates"][0]["mid"])

    def format_df(self) -> pd.DataFrame:
        df = self.df.dropna(subset=["id"]).copy()

        cols_to_format = [
            "averageDeadstockPrice",
            "highestBid",
            "lowestAsk",
            "price",
            "lastSale",
        ]
        for col in cols_to_format:
            # COLS WITH NUMBERS INTO FLOAT
            df.loc[:, col] = df[col].apply(lambda x: float(x))

            # COLS RENAMING
            new_col_name = f"{col}InPLN"
            df = df.rename(mapper={col: new_col_name})

            # USD TO PLN
            df.loc[:, new_col_name] = df[new_col_name].apply(
                lambda x: x * self.usd_to_pln
            ).round(2)

        df["priceDiffInPLN"] = df["lastSaleInPLN"] - df["price"]
        df["priceDiffInPLN"] = df["priceDiffInPLN"].round(2)

        return df

    def analyze(self) -> pd.DataFrame:
        df = self.format_df()
        df = df.loc[df["price_diff"] >= 100]

        return df
