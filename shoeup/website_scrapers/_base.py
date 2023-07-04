import abc
import logging

import requests


class BaseScraper(abc.ABC):
    def __init__(self):
        self.headers = {
            "accept": "application/json",
            "accept-encoding": "utf-8",
            "accept-language": "en-GB,en;q=0.9",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "x-requested-with": "XMLHttpRequest",
            "app-platform": "Iron",
            "app-version": "2022.05.08.04",
        }

    @abc.abstractmethod
    def run(self):
        pass

    @abc.abstractmethod
    def parse(self):
        pass

    def _get(self, params: dict) -> requests.Response:
        try:
            r = requests.get(self.url, params=params, headers=self.headers)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            logging.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            logging.error(f"Unknown Error: {err}")
