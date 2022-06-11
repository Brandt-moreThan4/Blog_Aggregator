"""High level module to run my scrapers. """

import logging
logging.basicConfig(filename='blog_aggregator/scrape.log',level=logging.DEBUG, filemode='w', format='%(name)s - %(levelname)s - %(message)s')

from settings import SITES_TO_SCRAPE
SITES_TO_SCRAPE = [5,7,8]


def scrape_new_data():

    for scraper in SITES_TO_SCRAPE:
        logging.info('!!info_message')
        try:
            5 + 'lol'
        except Exception as e:
            logging.error(f'{5+5}!!error_message',exc_info=True)
            print(str(e))
        5+5





if __name__ == '__main__':
    scrape_new_data()


