# ShoeUp

ShoeUp is a web scraping and analysis project focused on various shoe retail platforms. It scrapes data about shoes and analyzes prices to help you find the best deals. 

## Scraped Websites

The list of websites that the ShoeUp is currently scraping includes:

- [x] [StockX](https://stockx.com/)
- [x] [Adidas](https://www.adidas.pl/)
- [x] [Nike](https://www.nike.com/pl/)
- [x] [Eobuwie](https://eobuwie.com.pl/)
- [ ] [Miniramp](https://miniramp.pl/)
- [ ] [Snipes](https://www.snipes.pl/)
- [ ] [Adrenaline](https://adrenaline.pl/)
- [ ] [Nbsklep](https://nbsklep.pl/)
- [ ] [Zalando](https://www.zalando.pl/)
- [ ] [E-megasport](https://e-megasport.com/)
- [ ] [Zalando Lounge](https://www.zalando-lounge.pl/#/)
- [ ] [Vans](https://www.vans.pl/)
- [ ] [Converse](https://www.converse.pl/)
- [ ] [About You](https://www.aboutyou.pl/twoj-sklep)
- [ ] [Boozt](https://www.boozt.com/pl/pl)
- [ ] [Reebok](https://www.reebok.eu/en-pl/)

Each checkmark indicates that the scraper for that site is currently functional.

## Overview

Each website is handled by a separate scraper module that inherits from the base scraper class. For example, `StockX`, `Nike`, `Eobuwie`, and `Adidas` are handled by their respective classes. These classes are responsible for sending HTTP requests to the websites, handling the responses, and extracting the necessary data.

The data extracted by the scrapers are stored in pandas DataFrame objects. The extracted data include unique identifiers for the products, their prices, and links to their respective pages on the websites.

The scrapers are managed by a `main` module which initiates each scraper as a separate process, allowing them to run concurrently. The resulting DataFrames from each scraper are then merged and saved as .xlsx files for further processing.

An `Analyzer` class is used to analyze the merged data. It converts prices from USD to PLN (Polish Zloty), computes the final price after various taxes and fees, and highlights products with potential profitable price differences greater than 50, with volatility less than 1, and with at least one bid.

## Getting Started

1. Clone the repository.
2. Install the required dependencies listed in the `requirements.txt` file.
3. Run the `main.py` file to start scraping and analysis.

The program will log its progress and any issues encountered to `app.log`. The results of the scraping and analysis will be saved as .xlsx files.

## Note

Remember that web scraping should be performed in compliance with the terms and conditions of the websites being scraped, and with respect to their robots.txt files.

## Future Improvements

Work is ongoing to implement scraping for more websites as listed above. Additionally, improvements are planned for better error handling, more efficient data storage, and more detailed data analysis.
