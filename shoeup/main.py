import logging

import pandas as pd

import website_scrapers

logging.basicConfig(filename='app.log', filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG, datefmt='%d-%b-%y %H:%M:%S')

scrapers = {
    "nike": website_scrapers.NikeScraper(),
    'eobuwie': website_scrapers.Eobowie()
}


def main():
    logging.info('Start program')

    # GETTING MAIN DF FROM STOCKX
    stockx = website_scrapers.StockX()
    stockx_df = stockx.run()

    # RUN ALL SCRAPERS TO GET DFS AND CONCAT
    dfs = [scrapers[x].run() for x in scrapers]
    scrapers_df = pd.concat(dfs)

    logging.info('Saving scrapers df as xlsx')
    scrapers_df.to_excel('scrapers.xlsx', index=False)

    # MERGED DF FROM STOCKX WITH OTHER DFS FOR FURTHER ANALYZE
    logging.info('Start merging stockx df with scrapers df')
    merged_df = stockx_df.merge(
        scrapers_df, how="left", left_on="styleId", right_on="id"
    )
    logging.info('Saving merged df as xlsx')
    merged_df.to_excel("merged.xlsx", index=False)


if __name__ == "__main__":
    main()
