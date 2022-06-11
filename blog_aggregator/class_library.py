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

    pass
    # def get_new_posts(self):
    #     pass

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

    df_combined = pd.concat([df_db,df_new])

    df_combined.to_csv(data_path / 'article_db.csv',index=False)
    return df_combined
    # for posty in posty_list:
    #     print(f'Adding post: {posty}')


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


    def get_new_posts(self):
        """Check the RSS feed for any new posts and download those if they are newer than the newest in the db."""

        self.posts_on_feed = self.get_posts_on_feed()
        self.new_posts = [posty for posty in self.posts_on_feed if not post_is_in_db(posty)]

        add_posts_to_db(self.new_posts)


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


    def get_new_posts(self):
        """Check the RSS feed for any new posts and download those if they are newer than the newest in the db."""

        self.posts_on_feed = self.get_posts_on_feed()
        self.new_posts = [posty for posty in self.posts_on_feed if not post_is_in_db(posty)]

        add_posts_to_db(self.new_posts)


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

    # Name is used in several places to query the db for a specific blog.
    NAME = 'Aswath Damodaron Blog'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""

        self.most_recent_post = get_most_recent_post(self.NAME)

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        page_soup = sf.get_soup(self.BLOG_HOME)
        posts_on_page = page_soup.find_all(class_='post-outer')
        new_posts = [self.build_post(post_soup) for post_soup in posts_on_page
                     if self.get_post_date(post_soup) > self.most_recent_post.date]

        self.add_posts_to_db(new_posts)

    @staticmethod
    def get_post_date(post_soup):
        """Give the post soup and return a datetime.date object witht he post date. If 
            you can't get the date for some reason or can't parse it then just return a date of 1/1/1
            so it will be obvious something is screwey if it gets into the db, but most likely will not 
            get in since it only pulls in new posts."""

        try:
            date_string = post_soup.parent.parent.find(class_='date-header').text.strip()
            return parse(date_string).date()
        except:
            return datetime.date(1, 1, 1)

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = self.get_post_date(post_soup)
        new_post.title = post_soup.find(class_='post-title').text.strip()
        new_post.author = 'Aswath Damodaron'
        new_post.body = new_post.body = str(post_soup)
        new_post.url = post_soup.find(class_='post-title').a.get('href')
        new_post.website = self.ROOT_URL
        new_post.name = 'Aswath Damodaron Blog'

        return new_post

    def get_historical_posts(self):
        """Scrape all historical posts."""

        # YEARS and MONTHS are used to loop through all of the blog urls.
        YEARS = [str(2008 + i) for i in range(13)]
        MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

        for year in YEARS:
            for month in MONTHS:
                page_url = self.BLOG_HOME + '/' + year + '/' + month
                posts_on_page = self.get_posts_on_page(page_url)
                if posts_on_page:
                    self.add_posts_to_db(posts_on_page)
                # Take a short break to hopefully not be too much of a dick.
                time.sleep(4)

    def get_posts_on_page(self, page_url):
        """Given a url, extract all the post on the page and build the 
        posty object if the page actually contains posts."""

        page_soup = sf.get_soup(page_url)

        if self.page_is_valid(page_soup):
            return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post-outer')]

    @staticmethod
    def page_is_valid(page_soup):
        """Give the whole soup on the page and returns True if it contains at least one post on the page."""
        return page_soup.find(class_='post-body') is not None


class OSAMScraper(SiteScrapper):
    """Inherits from . Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://osam.com'
    BLOG_HOME = 'https://osam.com/Commentary'
    NAME = 'OSAM'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""
        self.most_recent_post = self.most_recent_post = get_most_recent_post(self.NAME)

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        page_soup = sf.get_soup(self.BLOG_HOME)
        posts_on_page = page_soup.find_all(class_='blogHeader')[:5]  # Just look at first 5
        new_posts = [self.build_post(post_soup) for post_soup in posts_on_page
                     if not self.is_in_db(post_soup)]

        self.add_posts_to_db(new_posts)


    @staticmethod
    def get_title(post_soup):
        return post_soup.h5.text

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = self.get_post_date(post_soup)
        new_post.title = self.get_title(post_soup)
        new_post.url = self.ROOT_URL + post_soup.a['href']

        # Can't find author or body from the Commentary archive page.
        page_soup = sf.get_soup(new_post.url).find(id='divcontent')
        new_post.author = page_soup.h1.find_next().text
        new_post.body = str(page_soup)
        new_post.website = self.ROOT_URL
        new_post.name = 'OSAM'

        return new_post


    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        posts = []
        for index, post_soup in enumerate(page_soup.find_all(class_='blogHeader')):
            try:
                posts.append(self.build_post(post_soup))

            except:
                print(f'Something screwed up for post {index + 1} which is: {post_soup.find("h5")}')
            time.sleep(4)

        return posts

class AlphaArchScraper(SiteScrapper):
    pass




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
