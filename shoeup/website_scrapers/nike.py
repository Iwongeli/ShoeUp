import json
from time import sleep
import requests
from website_scrapers._base import BaseScraper


class NikeScraper(BaseScraper):
    url = "https://api.nike.com/cic/browse/v2"

    def parse(self):
        pass

    def run(self):
        pass


def call_API(url):
    # NIKE API CALL
    html = requests.get(url=url, timeout=3)
    output = json.loads(html.text)
    return output


def loop_shoes(output):
    shoes = {}
    for item in output["data"]["products"]["products"]:
        if item["inStock"] is True and item["productType"] == "FOOTWEAR":
            title = item["title"]
            shoeId = item["url"].split("/")[-1]
            shoeLink = "https://www.nike.com/pl/" + item["url"][14:]
            print(shoeId, title, item["price"]["currentPrice"], shoeLink)
            shoes[shoeId] = title, item["price"]["currentPrice"], shoeLink
    return shoes


def main():
    res = {}
    # GET request
    # 60 ~ max that can be returned at one call
    count = 40
    anchor = 0
    country = "pl"
    country_language = "pl"
    query = "jordan"
    url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=241B0FAA1AC3D3CB734EA4B24C8C910D&country={country}&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace({country})%26filter%3Dlanguage({country_language})%26filter%3DemployeePrice(true)%26searchTerms%3D{query}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language={country_language}&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"
    html = requests.get(url=url, timeout=3)
    output = json.loads(html.text)
    totalPages = output["data"]["products"]["pages"]["totalPages"]
    sleep(1)

    for i in range(2):
        print("---------- PAGE NUMBER:", i + 1, "----------")
        url = f"https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=241B0FAA1AC3D3CB734EA4B24C8C910D&country={country}&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace({country})%26filter%3Dlanguage({country_language})%26filter%3DemployeePrice(true)%26searchTerms%3D{query}%26anchor%3D{anchor}%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D{count}&language={country_language}&localizedRangeStr=%7BlowestPrice%7D%E2%80%94%7BhighestPrice%7D"
        sleep(2)
        output = call_API(url)
        res.update(loop_shoes(output))
        anchor += count
        sleep(3)

    totalRecords = len(res.keys())
    print("----------SEARCH STATISTICS----------")
    print("total records:", totalRecords)
    print("lenght of page:", count)
    print("total pages:", totalPages)
    print("---------- END ----------")


if __name__ == "__main__":
    main()
