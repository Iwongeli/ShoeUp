import requests


def get_usd_to_pln():
    api = f"http://api.nbp.pl/api/exchangerates/rates/A/USD/"

    r = requests.get(api)

    return r.json()["mid"]
