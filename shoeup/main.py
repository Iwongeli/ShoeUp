import logging
from multiprocessing import Process, Manager
import multiprocessing.managers

import pandas as pd

import website_scrapers
from shoes_purchase_analyzer import Analyzer

LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATEFMT = "%d-%b-%y %H:%M:%S"
LOG_FILENAME = "app.log"

OUTPUT_FILENAME_SCRAPERS = "scrapers.xlsx"
OUTPUT_FILENAME_MERGED = "merged.xlsx"
OUTPUT_FILENAME_ANALYZED = "x.xlsx"

scrapers = (
    website_scrapers.StockX(),
    website_scrapers.Nike(),
    website_scrapers.Eobuwie(),
    website_scrapers.Adidas(),
)


def configure_logging():
    logging.basicConfig(
        filename=LOG_FILENAME,
        filemode="w",
        format=LOG_FORMAT,
        level=logging.DEBUG,
        datefmt=LOG_DATEFMT,
    )


def run_scrapers(manager: multiprocessing.managers.SyncManager):
    dfs_manager = manager.dict()
    processes = [Process(target=s.run, args=(dfs_manager,)) for s in scrapers]

    for process in processes:
        process.start()
    for process in processes:
        process.join()

    df_stockx = dfs_manager["StockX"]
    df_scrapers = pd.concat([v for k, v in dfs_manager.items() if k != "StockX"])

    return df_stockx, df_scrapers


def merge_dataframes(df_stockx, df_scrapers):
    return df_stockx.merge(df_scrapers, how="left", left_on="styleId", right_on="id")


def main():
    configure_logging()
    logging.info("Start program")

    with Manager() as manager:
        df_stockx, df_scrapers = run_scrapers(manager)
        logging.info("Saving scrapers df as xlsx")
        df_scrapers.to_excel(OUTPUT_FILENAME_SCRAPERS, index=False)

        logging.info("Start merging stockx df with scrapers df")
        df_merged = merge_dataframes(df_stockx, df_scrapers)
        logging.info("Saving merged df as xlsx")
        df_merged.to_excel(OUTPUT_FILENAME_MERGED, index=False)

        analyzer = Analyzer(df_merged)
        df_analyzed = analyzer.analyze()
        df_analyzed.to_excel(OUTPUT_FILENAME_ANALYZED, index=False)


if __name__ == "__main__":
    main()
