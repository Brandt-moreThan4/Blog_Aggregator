"""Library of all the scraping classes."""
import pandas as pd
import datetime
import json
from typing import List
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from dateutil.parser import parse

import scrapefunctions as sf
from utils import load_db, data_path

df_db = load_db()

class SiteScrapper:
    """Generic site scrapper that the rest will inherit from. This is kind of silly tho since the only method is
    a static method right?
    """

    def get_new_posts(self):
        """Check the RSS feed for any new posts and download those if they are newer than the newest in the db."""

        self.posts_on_feed = self.get_posts_on_feed()
        self.new_posts = [posty for posty in self.posts_on_feed if not post_is_in_db(posty)]

        add_posts_to_db(self.new_posts)    

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'



class Posty:
    """Class to store the information about each posts. It is basically just a dataclass."""

    # Only reason for doing below is that it is nice to know what this object should expect to have.
    _date: datetime.date
    title: str
    author: str
    url: str
    website_name: str

    def __init__(self):
        pass

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        """Try to convert the text date to datetime, but if it does not work then just default to today's date"""

        # If the value is already a date object and not a string, then don't try to convert it because
        # the parse function will throw an exception.
        if type(value) is datetime.datetime:
            # DJango model needs a datetime.date variable
            self._date = value.date()
        elif type(value) is datetime.date:
            self._date = value
        else:
            try:
                self._date = parse(value).date()
            except:
                # If convert doesn't work then just set it as the current time.
                self._date = datetime.date.today()

    def __str__(self):
        return f"{self.website_name}: {self.title}"


    def __repr__(self):
        return f"{self.website_name}: {self.title}"

    # I should also add in a magic method for dictionary like access?
    def as_dict(self):
        """Convert this instance to a dictionary"""
        return {'date': self.date, 'title': self.title, 'author': self.author, 'website_name': self.website_name, 'url':self.url}


    @staticmethod
    def from_series(row:pd.Series):
        post = Posty()
        post.date = row['date']
        post.title = row['title']
        post.website_name = row['website_name']
        post.author = row['author']
        post.url = row['url']

        return post

def add_posts_to_db(posty_list:List[Posty]):

    df_db = load_db()
    post_dicts = [posty.as_dict() for posty in posty_list]
    df_new = pd.DataFrame(post_dicts)

    if len(df_new) > 0:
        df_combined = pd.concat([df_db,df_new])

        df_combined.to_csv(data_path / 'article_db.csv',index=False)

    return df_new



class StratecheryScraper(SiteScrapper):
    ROOT_URL = 'https://stratechery.com/'
    BLOG_HOME = 'https://stratechery.com/category/articles'
    RSS_URL = 'https://rss.stratechery.passport.online/feed/rss/M5obc3noa81xuSLPuuEYif'

    WEBSITE_NAME = 'Stratechery'

    def __init__(self):
        pass

    def get_posts_on_feed(self) -> List[Posty]:
        """Extract all articles in the RSS feed and convert them to Posty objects."""

        rss_soup = sf.get_soup(self.RSS_URL,'xml')
        return [self.build_post(post_soup) for post_soup in rss_soup.find_all('item')]


    def build_post(self, post_soup:BeautifulSoup) -> Posty:
        """Send in the soup of an article and spit out a posty object with data filled in."""

        new_post = Posty()
        new_post.date = parse(post_soup.find('pubDate').text).date()
        new_post.title = post_soup.find('title').text
        new_post.author = post_soup.find('author').text
        new_post.url = post_soup.find('guid').text
        new_post.website_name = self.WEBSITE_NAME
        return new_post



class CollaborativeScraper(SiteScrapper):
    ROOT_URL = 'https://www.collaborativefund.com'
    BLOG_HOME = 'https://www.collaborativefund.com/blog/archive'
    RSS_URL = 'http://feeds.feedburner.com/collabfund'

    WEBSITE_NAME = 'Collaborative Fund'

    def __init__(self):
        pass



    def get_posts_on_feed(self) -> List[Posty]:
        """Extract all articles in the RSS feed and convert them to Posty objects."""

        rss_soup = sf.get_soup(self.RSS_URL,'lxml')
        return [self.build_post(post_soup) for post_soup in rss_soup.find_all('item')]


    def build_post(self, post_soup:BeautifulSoup) -> Posty:
        """Send in the soup of an article and spit out a posty object with data filled in."""

        new_post = Posty()
        new_post.date = parse(post_soup.find('pubdate').text).date()
        new_post.title = post_soup.find('title').text
        new_post.author = 'Unknown' # They don't provide the author in the feed unfortunately.
        new_post.url = post_soup.find('guid').text
        new_post.website_name = self.WEBSITE_NAME
        return new_post



class AswathScraper(SiteScrapper):
    """Implements specific functionality for scraping Aswath's website."""
    ROOT_URL = 'http://aswathdamodaran.blogspot.com'
    BLOG_HOME = 'http://aswathdamodaran.blogspot.com'

    NAME = 'Aswath Damodaron Blog'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""

        pass

    def get_new_posts(self):
        """Check the RSS feed for any new posts and download those if they are newer than the newest in the db."""

        self.posts_on_feed = self.get_posts_on_page(self.BLOG_HOME)
        self.new_posts = [posty for posty in self.posts_on_feed if not post_is_in_db(posty)]

        add_posts_to_db(self.new_posts)

    @staticmethod
    def build_post(post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = post_soup.parent.parent.find(class_='date-header').text.strip()
        new_post.title = post_soup.find(class_='post-title').text.strip()
        new_post.author = 'Aswath Damodaron'
        new_post.url = post_soup.find(class_='post-title').a.get('href')
        new_post.website_name = 'Aswath Damodaron Blog'

        return new_post


    def get_posts_on_page(page_url):
        """Given a url, extract all the post on the page and build the 
        posty object if the page actually contains posts."""

        page_soup = sf.get_soup(page_url)

        return [AswathScraper.build_post(post_soup) for post_soup in page_soup.find_all(class_='post-outer')]




class OSAMScraper(SiteScrapper):
    """Inherits from . Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://osam.com'
    BLOG_HOME = 'https://osam.com/Commentary'
    NAME = 'OSAM'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""
        pass


    def get_new_posts(self):
        """Check the RSS feed for any new posts and download those if they are newer than the newest in the db."""

        self.posts_on_feed = self.get_posts_on_page(self.BLOG_HOME)
        self.new_posts = [posty for posty in self.posts_on_feed if not post_is_in_db(posty)]

        add_posts_to_db(self.new_posts)

    @staticmethod
    def get_posts_on_page(page_url,posts_to_scape:int=20):
        """Given a url, extract all the post on the page and build the 
        posty objects if the page actually contains posts."""

        page_soup = sf.get_soup(page_url)
        return [OSAMScraper.build_post(post_soup) for post_soup in page_soup.find_all(class_='blogHeader')[:posts_to_scape]]

    @staticmethod
    def build_post(post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = post_soup.find(_class='divDate')
        new_post.title = post_soup.h5.text
        new_post.url = OSAMScraper.ROOT_URL + post_soup.a['href']

        # Can't find author or body from the Commentary archive page.
        page_soup = sf.get_soup(new_post.url).find(id='divcontent')
        new_post.author = page_soup.h1.find_next().text[3:] # Teh first 3 characters are not actually the author
        new_post.website_name = 'OSAM'

        return new_post


class MoneyBankingScaper(SiteScrapper):
    ROOT_URL = 'https://www.moneyandbanking.com/'
    BLOG_HOME = 'https://osam.com/Commentary'    
    RSS_URL = 'https://www.moneyandbanking.com/commentary?format=rss'
    WEBSITE_NAME = 'Money, Banking and Financial Markets'

    def __init__(self):
        pass

    @staticmethod
    def get_posts_on_feed() -> List[Posty]:
        """Extract all articles in the RSS feed and convert them to Posty objects."""

        rss_soup = sf.get_soup(MoneyBankingScaper.RSS_URL,'xml')
        return [MoneyBankingScaper.build_post(post_soup) for post_soup in rss_soup.find_all('item')]

    @staticmethod
    def build_post(post_soup:BeautifulSoup) -> Posty:
        """Send in the soup of an article and spit out a posty object with data filled in."""

        new_post = Posty()
        new_post.date = parse(post_soup.find('pubDate').text).date()
        new_post.title = post_soup.find('title').text
        new_post.author = post_soup.find('creator').text
        new_post.url = post_soup.find('link').text
        new_post.website_name = MoneyBankingScaper.WEBSITE_NAME
        return new_post



class AlphaArchScraper(SiteScrapper):
    pass
    # Scrape both blog and white papers




def get_most_recent_post(website_name: str = None) -> Posty:
    """Get the most recent post. Filtered by the name if one is passed in."""
    last_post_row:pd.Series = df_db.query(f'website_name == "{website_name}"').sort_values(by='date',ascending=False)
    posty = Posty.from_series(last_post_row)
    return posty


def post_is_in_db(posty:Posty) -> bool:
    """Test whether the post is in the db using either. I should update this to include the ability to filter by blog
     name as well."""

    df_filtered = df_db.query(f'website_name == "{posty.website_name}" & title == "{posty.title}" & author == "{posty.author}"')
    
    return len(df_filtered) > 0 
