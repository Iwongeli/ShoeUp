import time
from selenium import webdriver
from bs4 import BeautifulSoup
import json
import pandas as pd

def main():
    
    def get_data():
        # Provide the path to your ChromeDriver executable
        chrome_driver_path = r'C:\WebDriver\chromedriver.exe'

        # Create ChromeOptions and set the path to ChromeDriver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"

        # Initialize the WebDriver with the specified options
        driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

        query = 'jordan'
        resultsPerPage = '1000'
        url = f'https://stockx.com/api/browse?_search={query}&resultsPerPage={resultsPerPage}'
        print('Fetching data from:', url)

        driver.get(url)

        # Replace WebDriverWait with a sleep for a fixed duration (e.g., 5 seconds)
        time.sleep(2)  # Wait for 5 seconds

        # Get the page source
        page_source = driver.page_source

        # Use BeautifulSoup to parse the HTML and extract the JSON
        soup = BeautifulSoup(page_source, 'html.parser')
        json_data = soup.find('pre').text  # Extract the JSON content
        
        # Close the Selenium WebDriver when you're done
        driver.quit()
        
        # Convert the JSON data to a Python dictionary
        data_dict = json.loads(json_data)

        return data_dict


    def loop_data(data):
        product_list = []

        for product in data["Products"]:
            product_info = {
                "Title": product["title"],
                "shoeId": product["styleId"],
                "LowestAsk": product["market"]["lowestAsk"],
                "NumberOfAsks": product["market"]["numberOfAsks"],
                "LastSale": product["market"]["lastSale"],
                "lowestAskSize" : product["market"]["lowestAskSize"],
                "numberOfAsks" : product["market"]["numberOfAsks"],
                "hasAsks" : product["market"]["hasAsks"],
                "salesThisPeriod" : product["market"]["salesThisPeriod"],
                "salesLastPeriod" : product["market"]["salesLastPeriod"],
                "highestBid" : product["market"]["highestBid"],
                "highestBidSize" : product["market"]["highestBidSize"],
                "numberOfBids" : product["market"]["numberOfBids"],
                "hasBids" : product["market"]["hasBids"],
                "annualHigh" : product["market"]["annualHigh"],
                "annualLow" : product["market"]["annualLow"],
                "deadstockRangeLow" : product["market"]["deadstockRangeLow"],
                "deadstockRangeHigh" : product["market"]["deadstockRangeHigh"],
                "volatility" : product["market"]["volatility"],
                "deadstockSold" : product["market"]["deadstockSold"],
                "pricePremium" : product["market"]["pricePremium"],
                "averageDeadstockPrice" : product["market"]["averageDeadstockPrice"],
                "lastSale" : product["market"]["lastSale"],
                "lastSaleSize" : product["market"]["lastSaleSize"],
                "salesLast72Hours" : product["market"]["salesLast72Hours"],
                "changeValue" : product["market"]["changeValue"],
                "changePercentage" : product["market"]["changePercentage"],
                "absChangePercentage" : product["market"]["absChangePercentage"],
                "totalDollars" : product["market"]["totalDollars"],
                "lastLowestAskTime" : product["market"]["lastLowestAskTime"],
                "lastHighestBidTime" : product["market"]["lastHighestBidTime"],
                "lastSaleDate" : product["market"]["lastSaleDate"],
                "deadstockSoldRank" : product["market"]["deadstockSoldRank"]
            }
            product_list.append(product_info)

        df = pd.DataFrame(product_list)
        return df

    data = get_data()
    shoe_data = loop_data(data)
    print(shoe_data)
    return shoe_data


if __name__ == '__main__':
    main()