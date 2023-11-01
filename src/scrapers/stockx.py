"""StockX scraper module."""

import json
import logging
import time
from queue import Queue
from typing import Dict

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from ._base_scraper import BaseScraper

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class StockX:
    """Scraper for fetching shoe data from StockX."""

    def __init__(self, results_per_page: str = "1000"):
        """Initialize the scraper with search parameters."""
        logging.info("Initializing StockX scraper.")

        self.query = [
            "jordan",
            "nike",
            "adidas",
            "reebok",
            "puma",
            "new balance",
        ]
        self.results_per_page = results_per_page
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install())
        )

    def get_data(self, brand: str) -> Dict:
        """Fetch the raw data from the StockX API for a specific brand."""
        logging.info(f"Fetching data from StockX for brand {brand}.")

        url = f"https://stockx.com/api/browse?_search={brand}&resultsPerPage={self.results_per_page}"
        self.driver.get(url)
        time.sleep(2)  # Allow the page to load
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        json_data = soup.find("pre").text

        logging.info("Data fetched successfully.")
        return json.loads(json_data)

    def loop_data(self, data: Dict) -> pd.DataFrame:
        """Parse the raw data to create a DataFrame."""
        logging.info("Parsing raw data into DataFrame.")

        product_list = [
            {
                **{
                    "Title": product.get("title", None),
                    "styleId": product.get("styleId", None),
                },
                **{key: product["market"].get(key, None) for key in product["market"]},
            }
            for product in data["Products"]
        ]

        logging.info("Data parsed successfully.")
        return pd.DataFrame(product_list)

    def run(self, queue: Queue) -> None:
        """Main function that orchestrates the scraping process."""
        logging.info("Starting StockX scraper.")

        final_df = pd.DataFrame()

        for brand in self.query:
            data = self.get_data(brand)
            df = self.loop_data(data)

            final_df = pd.concat([final_df, df], ignore_index=True)

        if queue is not None:
            queue.put((self.__class__.__name__, final_df))
            logging.info("DataFrame added to queue.")

        self.driver.close()

        BaseScraper.save_file(final_df, self.__class__.__name__)

        logging.info("StockX scraper finished.")
