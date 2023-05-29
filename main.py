import requests
import json
import pandas as pd

def search(query):
    url = f'https://stockx.com/api/browse?_search={query}'

    headers = {
        'accept': 'application/json',
        'accept-encoding': 'utf-8',
        'accept-language': 'en-GB,en;q=0.9',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'x-requested-with': 'XMLHttpRequest',
        'app-platform': 'Iron',
        'app-version': '2022.05.08.04',
        'referer': 'https://stockx.com/'
    }

    r = requests.get(url=url, headers=headers)

    output = json.loads(r.text)
    data = {}

    # Add info from market to data dict
    for product in output['Products']:
        for key, value in product['market'].items():
            if key not in data:
                data[key] = []
            data[key].append(value)

    # Add rest of info to data dict
    for product in output['Products']:
        # Pop used dict
        if product['market']:
            product.pop('market')
        
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

# Call the search function with different query values
queries = ['dunk', 'jordan', 'yeezy']
dfs = []

for query in queries:
    df = search(query)
    dfs.append(df)

# Concatenate all dataframes into one
result_df = pd.concat(dfs, ignore_index=True)

# Save the concatenated dataframe to Excel
result_df.to_excel('output.xlsx', index=False)

print(result_df)
