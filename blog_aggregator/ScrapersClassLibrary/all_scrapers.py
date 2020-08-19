"""Aswath scraper"""

import time
from pathlib import Path
import sqlite3

from bs4 import BeautifulSoup

import temp_setup

from django.template.loader import get_template
from ScrapersClassLibrary.scrapers_class_lib import SiteScraper, Post
import scrapefunctions as sf


class AswathScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""
    ROOT_URL = 'http://aswathdamodaran.blogspot.com'
    BLOG_HOME = 'http://aswathdamodaran.blogspot.com'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Aswath Damodaron Blog'

    # YEARS and MONTHS are used to loop through all of the blog urls.
    # YEARS = [str(2008 + i) for i in range(12)]
    # MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    YEARS = ['2015']
    MONTHS = ['12']

    def get_historical_posts(self, years=YEARS, months=MONTHS):
        """Scrape all historical posts."""

        for year in years:
            for month in months:
                page_url = self.BLOG_HOME + '/' + year + '/' + month
                posts_on_page = self.get_posts_on_page(page_url)
                if posts_on_page:
                    self.add_posts_to_db(posts_on_page)
                time.sleep(3)

    def get_posts_on_page(self, page_url):
        """Given a url, extract all the post on the page if the page actually contains posts."""
        page_soup = sf.get_soup(page_url)

        if self.page_is_valid(page_soup):
            return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post-outer')]
        else:
            # Only use below for debugging?
            print(f'This url was skipped because it was invalid: {page_url}')

    @staticmethod
    def page_is_valid(page_soup):
        """Give the whole soup on the page and returns True if it contains at least one post on the page."""
        return page_soup.find(class_='post-body') is not None

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = post_soup.parent.parent.find(class_='date-header').text.strip()
        new_post.title = post_soup.find(class_='post-title').text.strip()
        new_post.author = 'Aswath Damodaron'
        new_post.body = new_post.body = str(post_soup)
        new_post.url = post_soup.find(class_='post-title').a.get('href')
        new_post.website = self.ROOT_URL
        new_post.name = 'Aswath Damodaron Blog'

        return new_post

    @staticmethod
    def add_posts_to_db(posts):
        """Give a list of Post objects and add each to the db."""
        conn = sqlite3.connect('scrapey.db')
        cur = conn.cursor()

        for post in posts:
            cur.execute("""INSERT INTO Scrape_Posts (date, title, author, body, url, website) 
               VALUES(?, ?, ?, ?, ?, ?, ?);""", [post.date, post.title, post.author, post.body, post.url, post.website,
                                                 post.name])

        conn.commit()
        conn.close()


class EugeneScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://www.eugenewei.com'
    BLOG_HOME = ROOT_URL
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Eugene Wei Blog'

    def get_historical_posts(self):
        """Scrape all historical posts."""

        current_url = self.BLOG_HOME

        while True:
            print(f'Getting soup for {current_url}')
            page_soup = sf.get_soup(current_url)
            posts_on_page = self.get_posts_on_page(page_soup)
            self.add_posts_to_db(posts_on_page)

            try:
                current_url = self.ROOT_URL + page_soup.find(id='nextLink')['href']
            except:
                current_url = None

            time.sleep(2)
            # if current_url is None:
            if True:
                break

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = post_soup.footer.find(class_='date').text
        new_post.title = post_soup.header.h1.text
        new_post.author = 'Eugene Wei'
        self.clean_body_content(post_soup)
        new_post.body = str(post_soup)
        new_post.url = self.ROOT_URL + post_soup.h1.a.get('href')
        new_post.website = self.ROOT_URL
        new_post.name = 'Eugene Wei Blog'

        return new_post

    @staticmethod
    def clean_body_content(post_soup):
        """Just make the post soup in a better format for viewing on funwithbrandt"""
        EugeneScraper.clean_images(post_soup)
        # Probably insert a clean side note below?

    @staticmethod
    def clean_images(post_soup):
        """Makes sure the correct src attribute is specified in the image tags.
        This is needed because there is some javascript that loads the images I think which screws it up a bit
        if you just copy the image tag without also bringing in the js, which I do not.
        Also adding 'img-fluid' class to images to make them more manageable later on."""

        images = post_soup.find_all('img')
        for image in images:
            image.attrs = {'src': EugeneScraper.get_image_src(image),
                           'alt': 'Sorry Brandt screwed up this image somehow.',
                           'class': 'img-fluid'}
            image.parent.attrs = {'style': 'max-width:700px;'}

    @staticmethod
    def get_image_src(img_tag):
        """Hopefully get a valid url for the picture to use as the src.
        One of these should point to the url where the image is stored."""

        if img_tag.get('src') is not None:
            return img_tag['src']
        elif img_tag.get('data-src') is not None:
            return img_tag['data-src']
        elif img_tag.get('data-image') is not None:
            return img_tag['data-image']
        else:
            return ''


class StratecheryScraper(SiteScraper):
    ROOT_URL = 'https://stratechery.com/'
    BLOG_HOME = 'https://stratechery.com/category/articles'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Stratechery'

    # Declaring it up here so that all methods can use the chrome driver after it has been created.
    # This feels sloppy though?
    driver = None

    def get_historical_posts(self):
        """Scrape all historical posts."""

        # Navigate to blog home
        self.driver = sf.get_chrome_driver()
        current_url = self.BLOG_HOME

        # On each loop, get all posts on the page and then try to click previous post link
        while True:
            print(f'Getting posts for {current_url}')
            self.driver.get(current_url)
            page_soup = BeautifulSoup(self.driver.page_source)
            posts_on_page = self.get_posts_on_page(page_soup)
            self.add_posts_to_db(posts_on_page)

            try:
                current_url = page_soup.find(class_='nav-previous').a['href']
            except:
                current_url = None

            if current_url is None:
                break

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        return [self.build_post(post_soup) for post_soup in page_soup.find_all('article')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""

        new_post = Post()
        new_post.date = post_soup.time.text
        new_post.title = post_soup.h1.text
        new_post.author = 'Ben Thompson'
        new_post.url = post_soup.a['href']
        new_post.body = self.get_content(new_post.url)
        new_post.website = self.ROOT_URL
        new_post.name = 'Stratechery'
        time.sleep(2)
        return new_post

    def get_content(self, post_url):
        self.driver.get(post_url)
        page_soup = BeautifulSoup(self.driver.page_source)

        return str(page_soup.article)


class CollaborativeScraper(SiteScraper):
    ROOT_URL = 'https://www.collaborativefund.com'
    BLOG_HOME = 'https://www.collaborativefund.com/blog/archive'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Collaberative Fund'

    # Declaring it up here so that all methods can use the chrome driver after it has been created.
    # This feels sloppy though?
    driver = None

    def get_historical_posts(self):
        """Scrape all historical posts."""

        # Navigate to blog home
        self.driver = sf.get_chrome_driver()
        self.driver.get(self.BLOG_HOME)
        page_soup = BeautifulSoup(self.driver.page_source)
        posts_on_page = self.get_posts_on_page(page_soup)
        self.add_posts_to_db(posts_on_page)

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post-item')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = post_soup.time.text
        new_post.title = post_soup.h4.text
        new_post.author = post_soup.find(class_='js-author').text
        new_post.url = self.ROOT_URL + post_soup.a['href']
        new_post.body = self.get_content(new_post.url)
        new_post.website = self.ROOT_URL
        new_post.name = 'Collaberative Fund'
        time.sleep(2)
        return new_post

    def get_content(self, post_url):
        self.driver.get(post_url)
        page_soup = BeautifulSoup(self.driver.page_source)
        CollaborativeScraper.clean_images(page_soup.article)
        return str(page_soup.article)

    @staticmethod
    def clean_images(post_soup):
        images = post_soup.find_all('img')
        for image in images:
            image.attrs = {'src': CollaborativeScraper.get_image_src(image),
                           'alt': 'Sorry Brandt screwed up this image somehow.',
                           'class': 'img-fluid'}


class OSAMScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://osam.com'
    BLOG_HOME = 'https://osam.com/Commentary'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'OSAM'

    def get_historical_posts(self):
        """Scrape all historical posts."""

        page_soup = sf.get_soup(self.BLOG_HOME)
        posts_on_page = self.get_posts_on_page(page_soup)
        self.add_posts_to_db(posts_on_page)

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='blogHeader')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = post_soup.find(class_='divDate').text.strip()
        new_post.title = post_soup.h5.text
        new_post.url = self.ROOT_URL + post_soup.a['href']

        # Can't find author or body from the Commentary archive page.
        page_soup = sf.get_soup(new_post.url).find(id='divcontent')
        new_post.author = page_soup.h1.find_next().text
        new_post.body = str(page_soup)
        new_post.website = self.ROOT_URL
        new_post.name = 'OSAM'

        return new_post


if __name__ == '__main__':
    test = OSAMScraper()
    test.get_historical_posts()
    test.make_html(name=test.NAME, folder_name='osam_posts', template_name='osam')
