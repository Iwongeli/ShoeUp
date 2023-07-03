import logging

import pandas as pd
import requests


class Analyzer:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.transaction_fee = 0.09
        self.payment_proc = 0.03
        self._usd_to_pln = None

    @property
    def usd_to_pln(self):
        if self._usd_to_pln is None:
            try:
                api = "http://api.nbp.pl/api/exchangerates/rates/A/USD/"
                r = requests.get(api)
                r.raise_for_status()
                self._usd_to_pln = float(r.json()["rates"][0]["mid"])
            except requests.RequestException:
                logging.warning("Error fetching exchange rate, defaulting to 4.")
                self._usd_to_pln = 4
        return self._usd_to_pln

    def usd_prices_to_pln(self, df: pd.DataFrame, columns: list) -> pd.DataFrame:
        df = df.copy()
        for column in columns:
            df[column] = df[column].apply(lambda x: float(x) * self.usd_to_pln).round(2)
        return df

    def format_df(self) -> pd.DataFrame:
        df = self.df.dropna(subset=["id"]).copy()

        cols_to_format = [
            "averageDeadstockPrice",
            "highestBid",
            "lowestAsk",
            "volatility",
            "lastSale",
        ]

        df = self.usd_prices_to_pln(df=df, columns=cols_to_format)

        df = df.assign(
            finalPriceAfterTaxes=(
                df["averageDeadstockPrice"]
                - (df["averageDeadstockPrice"] * self.payment_proc)
                - (df["averageDeadstockPrice"] * self.transaction_fee)
                - 5.45 * self.usd_to_pln  # 5.45 is delivery cost
            ).round(2),
        )

        return df

    def analyze(self) -> pd.DataFrame:
        df = self.format_df()
        df = df.assign(
            priceDiff=lambda df: df.finalPriceAfterTaxes - df.price,
        )
        return df[(df.priceDiff > 50) & (df.numberOfBids > 0) & (df.volatility < 1)]
