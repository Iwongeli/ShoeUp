import logging
import pandas as pd
import requests
import json
from time import sleep

from _base import BaseScraper


class Reebok(BaseScraper):
    def __init__(self) -> None:
        super().__init__()
        self.headers = {
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
            "Dnt": "1",
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": "Android",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
            # necessary
            "X-Castle-Request-Token": "SUAfcDAwBDl9OxEwfyF-MTozBw8hAXwwED4oMw4QHAJ9LgEGUOMl5IUYAefzjXt1gqCpA8H-CdR_A1YEPgtKEzpwJipvTFRXGIMbhKYtUjI3Pl5AxwQVCz9_LQa8TSV9VmwmZhA1ZDcfKAZuUXUyPB9BJGNNbyNjHzZkNwQgBGJHdTknCiAIclZsLihyUgsyB05jJ35wOmtaVy9ldGk-KAozfSkMNmovdEgeSnMsamtWay8neGUpbFApakRXciVqWi97NgsueikPLnoncm8oblNlalReZit1Vi9_NAgueTFTCC43WWMpNw04PQQ4esEHqwhyNQxifmMPMtZMfk4NS3ogYk5RdC9rEyADaUtlJi9tKWpOTWk5L20pal9aIA11XnAiblxzakNWci9kSzMONg4gPHRgNRU3H3A5WApfeisfRHlDDjFjoywxZDcOLns-CDBmJw8xcDcPOno3kAhKsh7F_Az0AJkG4oMq4DjrSfBwzk-Hrf_gbbwDSgsyRT91UHAvKGhhOHRed14WT2xnV3MsOmsTZSQqalNmYlFASgc_AEoHPwBKBz8ASgc_AEoHPwBKBz8ASgc_AEoHPwBKR39ACkd_AEoHPwBKBz8ASgc_QEoHPwBKBz8ASgc___M",
        }

    def parse(self, response: requests.Response) -> pd.DataFrame:
        decoded_content = response.content.decode('utf-8')
        result = json.loads(decoded_content)

        data = {"id": [], "price": [], "link": []}

        data["link"].append(result['product']['slug'])
        data["id"].append(result['product']['result']['brandStyleId'])
        data["price"].append(result['product']['price']['formattedPrice'])

        return pd.DataFrame(data)

    def run(self) -> pd.DataFrame:
        logging.info("Start scraping %s", self.__class__.__name__)

        # take file with links to shoes and process it
        with open("shoeup/tools/reebok/href_values.csv") as f:
            data = {"id": [], "price": [], "link": []}
            for link in f:
                link = link.rstrip()
                # link + address to run api
                url_with_param = link + "?_data=routes%2F%24subfolder%2Fshopping%2F%24"
                # sleep for safety reasons if needed
                sleep(3)
                response = requests.get(url=url_with_param, headers=self.headers)
                df = self.parse(response)
                data["link"].extend(df["link"])
                data["id"].extend(df["id"])
                data["price"].extend(df["price"])

        df_reebok = pd.DataFrame(data)
        df_reebok["shop"] = self.__class__.__name__
      
        return df_reebok
