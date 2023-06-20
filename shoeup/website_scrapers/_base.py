import abc
import requests


class BaseScraper(abc.ABC):
    headers = {
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
        r = requests.get(self.url, params=params, headers=self.headers)
        r.raise_for_status()

        return r
