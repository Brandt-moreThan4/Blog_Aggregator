"""High level module to run my scrapers. """
from django import db
import pandas as pd
import logging
from pathlib import Path

from utils import load_db, create_db
from typing import List

import class_library
from class_library import StratecheryScraper, CollaborativeScraper, AswathScraper, OSAMScraper, SiteScrapper, MoneyBankingScaper, OakTreeScraper


# logging.basicConfig(filename='blog_aggregator/scrape.log',level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO)




# Perhaps the sites to scrape should actually be a setting that could be turned on and off in the db.
SITES_TO_SCRAPE:List[SiteScrapper] = [StratecheryScraper, CollaborativeScraper, AswathScraper,
                                     OSAMScraper, MoneyBankingScaper, OakTreeScraper]

# SITES_TO_SCRAPE = [class_library.AlphaArchScraper]


def scrape_new_data():

    try:
        df_data = load_db()
    except:
        logging.info(f'Creating a new db, because there is not an existing one.')
        df_data = create_db() 
    
    old_post_count = len(df_data)
    for scraper in SITES_TO_SCRAPE:
        logging.info(f'About to try to scrape{scraper}')
        scraper = scraper()
        scraper.get_new_posts()

    
    


if __name__ == '__main__':

    scrape_new_data()


    print('scraping is done!')