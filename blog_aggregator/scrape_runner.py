"""High level module to run my scrapers. """
import pandas as pd
import logging
from email_sender import email_new_posts
from utils import load_db, create_db, MissingDbException
from typing import List
import datetime

from class_library import StratecheryScraper, CollaborativeScraper, AswathScraper, OSAMScraper, SiteScrapper, MoneyBankingScaper, OakTreeScraper


logging.basicConfig(filename='blog_aggregator/scrape.log',level=logging.INFO, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.INFO)


# Perhaps the sites to scrape should actually be a setting that could be turned on and off in the db.
SITES_TO_SCRAPE:List[SiteScrapper] = [StratecheryScraper, CollaborativeScraper, AswathScraper,
                                     OSAMScraper, MoneyBankingScaper, OakTreeScraper]

# SITES_TO_SCRAPE = [OSAMScraper, OakTreeScraper]


def scrape_new_data():
    logging.info(f'Beginning the scraping process at.')

    # Theoreitcally, I should reload the db after each scraper has updated the db.
    try:
        df_data_old = load_db()
    except MissingDbException as e:
        logging.info(f'Creating a new db, because there is not an existing one.')
        df_data_old = create_db() 
    
    for scraper in SITES_TO_SCRAPE:
        scraper = scraper(df_db=df_data_old)
        logging.info(f'About to try to scrape {scraper}')
        scraper.get_new_posts()
        scraper.add_posts_to_db()
    
    logging.info(f'Finishing the scraping process at.')

    df_data_new = load_db()

    if len(df_data_new) > len(df_data_old):
        logging.info('Yipee, looks like there are new posts. Now we can send an email.')
        df_new_posts_only = df_data_new[~df_data_new.title.isin(df_data_old.title)]
        email_new_posts(df_new_posts_only)



if __name__ == '__main__':

    scrape_new_data()

    print('scraping is done!')