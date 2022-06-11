"""High level module to run my scrapers. """
import pandas as pd
import logging
from pathlib import Path

from utils import load_db


logging.basicConfig(filename='blog_aggregator/scrape.log',level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

from settings import SITES_TO_SCRAPE
# SITES_TO_SCRAPE = [5,7,8]




def scrape_new_data():

    df_data = load_db() 
    old_post_count = len(df_data)
    for scraper in SITES_TO_SCRAPE:
        scraper = scraper()
        scraper.get_new_posts()

    
    


if __name__ == '__main__':

    scrape_new_data()


