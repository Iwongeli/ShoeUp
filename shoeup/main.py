import logging
from multiprocessing import Process, Manager

import pandas as pd

import website_scrapers

logging.basicConfig(
    filename="app.log",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    datefmt="%d-%b-%y %H:%M:%S",
)

scrapers = (
    website_scrapers.StockX(),
    website_scrapers.Nike(),
    website_scrapers.Eobuwie(),
)


def main():
    logging.info("Start program")

    # RUN ALL SCRAPERS TO GET DFS AND CONCAT
    with Manager() as manager:
        dfs_manager = manager.dict()

        processes = [Process(target=s.run, args=(dfs_manager,)) for s in scrapers]

        for process in processes:
            process.start()

        for process in processes:
            process.join()

        df_stockx = dfs_manager["StockX"]
        df_scrapers = pd.concat([v for k, v in dfs_manager.items() if k != "StockX"])

    logging.info("Saving scrapers df as xlsx")
    df_scrapers.to_excel("scrapers.xlsx", index=False)

    # MERGED DF FROM STOCKX WITH OTHER DFS FOR FURTHER ANALYZE
    logging.info("Start merging stockx df with scrapers df")
    df_merged = df_stockx.merge(
        df_scrapers, how="left", left_on="styleId", right_on="id"
    )
    logging.info("Saving merged df as xlsx")
    df_merged.to_excel("merged.xlsx", index=False)


if __name__ == "__main__":
    main()
