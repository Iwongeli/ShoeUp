import json
from time import sleep
import pandas as pd
import requests


USD_PLN = 4.08


def total_records(query, page, resultsPerPage):
    url = f"https://stockx.com/api/browse?_search={query}&page={page}&resultsPerPage={resultsPerPage}"

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
        "referer": "https://stockx.com/",
    }

    r = requests.get(url=url, headers=headers, timeout=3)

    output = json.loads(r.text)
    total_pages = output['Pagination']['total']
    return total_pages
    

def search(query, page, resultsPerPage):
    url = f"https://stockx.com/api/browse?_search={query}&page={page}&resultsPerPage={resultsPerPage}"
    print(url)

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
        "referer": "https://stockx.com/",
    }

    r = requests.get(url=url, headers=headers, timeout=3)

    output = json.loads(r.text)
    data = {}
    
    # Add info from market to data dict
    for product in output["Products"]:
        for key, value in product["market"].items():
            if key not in data:
                data[key] = []
            data[key].append(value)

    # Add rest of info to data dict
    for product in output["Products"]:
        # Pop used dict
        if product["market"]:
            product.pop("market")

        for key, value in product.items():
            if key not in data:
                data[key] = []
            data[key].append(value)

    # Fill missing values with None
    max_length = max(len(lst) for lst in data.values())
    for key in data:
        data[key] += [None] * (max_length - len(data[key]))

    df = pd.DataFrame(data)
    return df


def transform_records(df):
    res = {}
    counter = 0
    print('reference_price / revenue / avg_price / attractiveness')
    for row in df.itertuples():
        # Access data for each column in the current row
        shoe_id = row.styleId
        if len(shoe_id) < 2:
            print('error: no styleId')
            continue
        counter += 1
        reference_price = round((row.averageDeadstockPrice + row.highestBid + row.lastSale) / 3 * USD_PLN, 2)
        revenue = round(reference_price - (reference_price * 0.075 + reference_price * 0.03), 2)
        avg_price = round(row.averageDeadstockPrice * USD_PLN, 2)
        attractiveness = 1 * round((1 - row.volatility), 2)

        res[shoe_id] = (reference_price, revenue, avg_price, attractiveness)
        print(shoe_id, res[shoe_id])
        
    
    print('TRANSFORM RECORD: SUCCES')
    print('TOTAL RECORDS:', counter)


def main():
    # Call the search function with different query values
    query = "puma"
    page = 1
    resultsPerPage = 40
    dfs = []
    pages = int(total_records(query, page, resultsPerPage) / resultsPerPage) - 1
    print('QUERY:', query, '\nRESULTS PER PAGE:', resultsPerPage, '\nTOTAL PAGES:', pages)
    sleep(5)

    for i in range(1, 5):
        print('PROCESSING PAGE NR:', i)
        df = search(query, i, resultsPerPage)
        dfs.append(df)
        sleep(5)

    # Concatenate all dataframes into one
    print('TRANSFORMING RECORDS...')
    result_df = pd.concat(dfs, ignore_index=True)
    transform_records(result_df)



if __name__ == '__main__':
    main()