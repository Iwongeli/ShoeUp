import json
import pandas as pd
from time import sleep
import requests

def main():
    def call_API(url):
        # NIKE API CALL
        html = requests.get(url=url, timeout=3)
        output = json.loads(html.text)
        return output

    def loop_shoes(output):
        data = {
            'shoeId': [],
            'title': [],
            'price': [],
            'shoeLink': []
        }

        for item in output['data']['products']['products']:
            if item['inStock'] is True and item['productType'] == 'FOOTWEAR':
                title = item['title']
                shoeId = item['url'].split('/')[-1]
                shoeLink = 'https://www.nike.com/pl/' + item['url'][14:]
                price = item['price']['currentPrice']

                data['shoeId'].append(shoeId)
                data['title'].append(title)
                data['price'].append(price)
                data['shoeLink'].append(shoeLink)

        return pd.DataFrame(data)


    def get_shoe_data():
        res = pd.DataFrame()  # Initialize an empty DataFrame
        # GET request
        # 60 ~ max that can be returned at one call
        count = 60
        anchor = 0
        country = 'pl'
        country_language = 'pl'
        query = 'jordan'
        url = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=241B0FAA1AC3D3CB734EA4B24C8C910D&country={country}&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace({country})%26filter%3Dlanguage({country_language})%26filter%3DemployeePrice(true)%26searchTerms%3D{query}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language={country_language}&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D'
        html = requests.get(url=url, timeout=3)
        output = json.loads(html.text)
        totalPages = output['data']['products']['pages']['totalPages']
        sleep(1)

        for i in range(4):
            print('PAGE NUMBER:', i + 1)
            url = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=241B0FAA1AC3D3CB734EA4B24C8C910D&country={country}&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace({country})%26filter%3Dlanguage({country_language})%26filter%3DemployeePrice(true)%26searchTerms%3D{query}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language={country_language}&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D'
            sleep(2)
            output = call_API(url)
            res = pd.concat([res, loop_shoes(output)], ignore_index=True)
            anchor += count

        # Return the DataFrame with shoe data

        return pd.DataFrame(res)
    dataset = get_shoe_data()

    return dataset


if __name__ == '__main__':
    main()

