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
                time.sleep(4)

    def get_posts_on_page(self, page_url):
        """Given a url, extract all the post on the page if the page actually contains posts."""
        page_soup = sf.get_soup(page_url)

        if self.page_is_valid(page_soup):
            return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post-outer')]

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


class EugeneScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://www.eugenewei.com'
    BLOG_HOME = ROOT_URL
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Eugene Wei Blog'

    def get_historical_posts(self):
        """Scrape all historical posts."""

        current_url = self.BLOG_HOME
        # Oldest url that was not read is below link.
        # current_url = 'https://www.eugenewei.com/?offset=1411494003761'
        while current_url is not None:
            print(f'Getting soup for {current_url}')
            page_soup = sf.get_soup(current_url)
            if self.page_is_valid(page_soup):
                posts_on_page = self.get_posts_on_page(page_soup)
                self.add_posts_to_db(posts_on_page)
                time.sleep(15)
            else:
                print(f'Page is not valid for {current_url}')

            try:
                current_url = self.ROOT_URL + page_soup.find(id='nextLink')['href']
            except:
                current_url = None

    @staticmethod
    def page_is_valid(page_soup):
        """Give the whole soup on the page and returns True if it contains at least one post on the page."""
        return page_soup.find(class_='post') is not None

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""

        return [self.build_post(post_soup) for post_soup in page_soup.find_all(class_='post')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = self.get_date(post_soup)
        new_post.title = post_soup.header.h1.text
        new_post.author = 'Eugene Wei'
        self.clean_body_content(post_soup)
        new_post.body = str(post_soup)
        new_post.url = self.ROOT_URL + post_soup.h1.a.get('href')
        new_post.website = self.ROOT_URL
        new_post.name = 'Eugene Wei Blog'

        return new_post

    @staticmethod
    def get_date(post_soup):
        try:
            return post_soup.footer.find(class_='date').text
        except:
            return ''

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
        # As of 8/20/2020 there were 41 archive pages
        while current_url is not None:
            # print(f'Getting posts for {current_url}')
            self.driver.get(current_url)
            page_soup = BeautifulSoup(self.driver.page_source)
            posts_on_page = self.get_posts_on_page(page_soup)
            self.add_posts_to_db(posts_on_page)

            try:
                current_url = page_soup.find(class_='nav-previous').a['href']
            except:
                current_url = None

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
        time.sleep(10)
        return new_post

    def get_content(self, post_url):
        self.driver.get(post_url)
        page_soup = BeautifulSoup(self.driver.page_source)

        return str(page_soup.article)


class CollaborativeScraper(SiteScraper):
    ROOT_URL = 'https://www.collaborativefund.com'
    BLOG_HOME = 'https://www.collaborativefund.com/blog/archive'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Collaborative Fund'

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

        # Below loop is to break this into chunks so that you don't try to do the entire history in one go. Any error
        # Along the way would mean nothing is added to the database.
        posts_chunk = []
        for post_soup in posts_on_page:
            posts_chunk.append(self.build_post(post_soup))
            if len(posts_chunk) >= 50:
                self.add_posts_to_db(posts_chunk)
                posts_chunk = []

        if posts_chunk:
            self.add_posts_to_db(posts_chunk)

    @staticmethod
    def get_posts_on_page(page_soup):
        """Given a url, extract all the post on the page."""

        return [post_soup for post_soup in page_soup.find_all(class_='post-item')]

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        new_post.date = post_soup.time.text
        new_post.title = post_soup.h4.text
        new_post.author = post_soup.find(class_='js-author').text
        new_post.url = self.ROOT_URL + post_soup.a['href']
        new_post.body = self.get_content(new_post.url)
        new_post.website = self.ROOT_URL
        new_post.name = 'Collaborative Fund'
        time.sleep(4)
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

    @staticmethod
    def get_image_src(img_tag):
        """Hopefully get a valid url for the picture to use as the src"""
        try:
            return CollaborativeScraper.ROOT_URL + img_tag['src']
        except:
            return ''


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

        posts = []
        for index, post_soup in enumerate(page_soup.find_all(class_='blogHeader')):
            try:
                posts.append(self.build_post(post_soup))

            except:
                print(f'Something screwed up for post {index+1} which is: {post_soup.find("h5")}')
            time.sleep(4)

        return posts

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


class AmnesiaScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://investoramnesia.com'
    BLOG_HOME = 'https://investoramnesia.com/category/sunday-reads'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Amnesia'
    count = 0

    def get_historical_posts(self):
        """Scrape all historical posts."""
        """Insanely slow for some reason to get soup?"""
        current_url = self.BLOG_HOME

        while current_url is not None:
            print(f'About to try to get post on page: {current_url}')
            page_soup = sf.get_soup(current_url)
            posts_on_page = self.get_posts_on_page(page_soup)
            self.add_posts_to_db(posts_on_page)
            try:
                current_url = page_soup.find('a', class_='next')['href']
            except:
                current_url = None

    def get_posts_on_page(self, page_soup: BeautifulSoup) -> list:
        """Given a url, extract all the post on the page."""
        posts = []
        for index, post_soup in enumerate(page_soup.find_all(class_='post-content')):
            try:
                print(f'About to try for post: {index}')
                posts.append(self.build_post(post_soup))
            except:
                print(f'Something screwed up for post {index+1}')
            time.sleep(3)

        return posts

    def build_post(self, post_soup: BeautifulSoup) -> Post:
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Post()
        self.count += 1
        new_post.url = post_soup.a['href']

        page_soup = sf.get_soup(new_post.url)
        new_post.date = page_soup.find(class_='date').text.strip()
        new_post.title = page_soup.find(id='page-header-wrap').h1.text
        new_post.author = 'Jamie Catherwood'
        new_post.body = str(page_soup.find(class_='post-area'))
        new_post.website = self.ROOT_URL
        new_post.name = 'Amnesia'

        return new_post


class GatesScraper(SiteScraper):
    ROOT_URL = 'https://www.gatesnotes.com'
    BLOG_HOME = 'https://www.gatesnotes.com/All'

    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Gates Notes'

    # Declaring it up here so that all methods can use the chrome driver after it has been created.
    # This feels sloppy though?
    driver = None

    def get_historical_posts(self):
        """Only gets the posts on the first page. More post don't appear unless you scroll down to
        the bottom of the page."""

        # Navigate to blog home
        self.driver = sf.get_chrome_driver()
        current_url = self.BLOG_HOME

        while True:
            self.driver.get(current_url)
            time.sleep(4)
            page_soup = BeautifulSoup(self.driver.page_source)
            posts_on_page = self.get_posts_on_page(page_soup)
            self.add_posts_to_db(posts_on_page)

            break

    def get_posts_on_page(self, page_soup):
        """Given a url, extract all the post on the page."""
        posts = []
        for index, post_soup in enumerate(page_soup.find_all(class_='TGN_site_ArticleItemSearchThumb')):
            try:
                print(f'About to try for post: {index}')
                posts.append(self.build_post(post_soup))
            except:
                print(f'Something screwed up for post {index+1}')
            time.sleep(3)

        return posts

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""

        new_post = Post()
        new_post.url = self.ROOT_URL + post_soup.a['href']

        self.driver.get(new_post.url)
        page_soup = BeautifulSoup(self.driver.page_source)

        new_post.date = page_soup.find(class_='article_top_dateline').text
        new_post.title = page_soup.find(class_='article_top_head').text
        new_post.author = 'Bill Gates'

        new_post.body = str(page_soup.find(class_='TGN_site_Articlecollumn'))
        new_post.website = self.ROOT_URL
        new_post.name = 'Gates Notes'

        return new_post


# if __name__ == '__main__':
