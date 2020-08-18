"""Library of all the scraping classes"""

from abc import ABC, abstractmethod


class SiteScraper(ABC):
    """Generic scraper with properties that all scrapers should have."""
    ROOT_URL = None
    BLOG_HOME = None

    def get_historical_posts(self):
        pass

    def build_post(self):
        pass


class Post:
    date = ''
    title = ''
    author = ''
    body = ''
    url = ''
    website = ''


    # # Make date property instead
    # def convert_date(self):
    #     """Try to convert the text date to datetime, but if it does not work then keep it
    #     as a string"""
    #     # This is sketch. I should not allow the possibility for self.date to be two different types.
    #     try:
    #         self.date = datetime.datetime.strptime(self.date, '%A, %B %d, %Y')
    #     except:
    #         pass

    # def __str__(self):
    #     return str(f'{self.date}\n{self.title}\n{self.body}')

