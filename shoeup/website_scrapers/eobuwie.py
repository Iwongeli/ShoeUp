import logging

import pandas as pd
import requests

from website_scrapers._base import BaseScraper


class Eobowie(BaseScraper):
    url = 'https://eobuwie.com.pl/t-api/rest/search/eobuwie/v4/search'

    def __init__(self) -> None:
        self.dfs = []

    def run(self) -> pd.DataFrame:
        logging.info('Start scraping Nike')

        params = {'channel': 'eobuwie',
                  'currency': 'PLN',
                  'locale': 'pl_PL',
                  'limit': 48,
                  'page': 1,
                  'categories[]': 'meskie/polbuty/sneakersy',
                  'select[]': ['model', 'final_price', 'url_key']}

        while True:
            df = self.parse(self._get(params=params))

            if df.empty is False:
                self.dfs.append(df)
                params['page'] += 1
            else:
                break

        return pd.concat(self.dfs)

    def parse(self, response: requests.Response) -> pd.DataFrame:
        def parse_model(value):
            model_list = value.split()
            if len(model_list[-1]) < 5 and len(model_list) > 2:
                return model_list[-2] + '-' + model_list[-1]
            else:
                return model_list[-1]

        data = {"id": [], "price": [], "link": []}

        products = response.json()['products']
        if len(products) > 0:
            for product in products:
                data['id'].append(parse_model(
                    product['values']['model']['value']))
                data['price'].append(
                    product['values']['final_price']['value']['pl_PL']['PLN']['amount'])
                data['link'].append('https://eobuwie.com.pl/p/' +
                                    product['values']['url_key']['value']['pl_PL'])
        else:
            data = {}

        return pd.DataFrame(data)
