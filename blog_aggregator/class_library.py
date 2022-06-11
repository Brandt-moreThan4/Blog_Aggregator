"""Library of all the scraping classes."""

import datetime
import json
import requests
from pathlib import Path
import time
from bs4 import BeautifulSoup
from dateutil.parser import parse
from django.utils.text import slugify

import scrapefunctions as sf

LOG_FILE = Path(__file__).parent / 'error_log.txt'
WEB_ROOT = 'https://www.funwithbrandt.com/'


class SiteScrapper:
    """Generic site scrapper that the rest will inherit from. This is kind of silly tho since the only method is
    a static method right?
    """

    @staticmethod
    def add_posts_to_db(posts: list):

        for posty in posts:

            response = requests.post(WEB_ROOT + '/api/blog-external-list/', posty.as_dict())
            if response != 201:
                try:
                    error_msg = (f"{datetime.datetime.now()}--Well Shit. Something screwed up when trying to " +
                                 f"add the following post to the db: \n {str(posty)}\n")
                except:
                    # In case there is trouble representing the post as as a string.
                    error_msg = (
                        f"{datetime.datetime.now()}--Well Shit. Something screwed up when trying to add posts to db")

                with LOG_FILE.open('a') as f:
                    f.write(error_msg)
            else:
                print(f'Successfully uploaded:\n{posty}\n')



class Posty:
    """Love this"""

    _date: datetime.date
    title: str
    author: str
    body: str
    url: str
    website: str
    name: str
    soup: BeautifulSoup

    def __init__(self, json_str: str = None):
        if json_str:
            self.load_json(json_str)

    def load_json(self, json_str):
        """Input a json string and use it to populate this posty"""
        json_dick = json.loads(json_str)
        self.date = json_dick.get('date')
        self.title = json_dick.get('title')
        self.author = json_dick.get('author')
        self.body = json_dick.get('body')
        self.url = json_dick.get('url')
        self.website = json_dick.get('website')
        self.name = json_dick.get('name')

    @property
    def slug(self):
        """make a slug out of title"""
        return slugify(self.title)

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
        return f"{self.name};{self.title}"

    def as_dict(self):
        """Convert this instance to a dictionary"""
        return {'date': self.date, 'title': self.title, 'author': self.author,
                'body': self.body, 'url': self.url, 'website': self.website,
                'name': self.name, 'slug': self.slug}


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


class EugeneScraper(SiteScrapper):
    """Fun stuff"""

    ROOT_URL = 'https://www.eugenewei.com'
    BLOG_HOME = ROOT_URL
    # Name is used in several places to query the db for a specific blog.
    NAME = 'Eugene Wei Blog'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""
        self.most_recent_post = get_most_recent_post(self.NAME)

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        page_soup = sf.get_soup(self.BLOG_HOME)
        posts_on_page = page_soup.find_all(class_='post')
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
            date_string = post_soup.footer.find(class_='date').text.strip()
            return parse(date_string).date()
        except:
            return datetime.date(1, 1, 1)

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = self.get_post_date(post_soup)
        new_post.title = post_soup.header.h1.text
        new_post.author = 'Eugene Wei'
        self.clean_images(post_soup)
        new_post.body = str(post_soup)
        new_post.url = self.ROOT_URL + post_soup.h1.a.get('href')
        new_post.website = self.ROOT_URL
        new_post.name = 'Eugene Wei Blog'

        return new_post

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

    def get_historical_posts(self):
        """Scrape all historical posts."""

        current_url = self.BLOG_HOME

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


class StratecheryScraper(SiteScrapper):
    ROOT_URL = 'https://stratechery.com/'
    BLOG_HOME = 'https://stratechery.com/category/articles'
    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Stratechery'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object.
            and get the chrome driver up and running.
        """
        self.most_recent_post = get_most_recent_post(self.NAME)
        # Declaring it up here so that all methods can use the chrome driver after it has been created.
        self.driver = sf.get_chrome_driver()

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        self.driver.get(self.BLOG_HOME)
        page_soup = BeautifulSoup(self.driver.page_source)
        posts_on_page = page_soup.find_all('article')
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
            date_string = post_soup.time.text.strip()
            return parse(date_string).date()
        except:
            return datetime.date(1, 1, 1)

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""

        new_post = Posty()
        new_post.date = self.get_post_date(post_soup)
        new_post.title = post_soup.h1.text
        new_post.author = 'Ben Thompson'
        new_post.url = post_soup.a['href']
        new_post.body = self.get_content(new_post.url)
        new_post.website = self.ROOT_URL
        new_post.name = 'Stratechery'
        # Remember to try not be a dick!
        time.sleep(3)
        return new_post

    def get_content(self, post_url):
        self.driver.get(post_url)
        page_soup = BeautifulSoup(self.driver.page_source)

        return str(page_soup.article)

    def get_historical_posts(self):
        """Scrape all historical posts."""

        # Start on the first page
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


class CollaborativeScraper(SiteScrapper):
    ROOT_URL = 'https://www.collaborativefund.com'
    BLOG_HOME = 'https://www.collaborativefund.com/blog/archive'

    NAME = 'Collaborative Fund'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object.
            and get the chrome driver up and running.
        """
        self.most_recent_post = self.most_recent_post = get_most_recent_post(self.NAME)
        # Declaring it up here so that all methods can use the chrome driver after it has been created.
        self.driver = sf.get_chrome_driver()

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db.
            Also get that driver cranked up.
        """

        self.driver.get(self.BLOG_HOME)
        page_soup = BeautifulSoup(self.driver.page_source)
        posts_on_page = page_soup.find_all(class_='post-item')[:15]  # Only look at the most recent 15
        new_posts = [self.build_post(post_soup) for post_soup in posts_on_page
                     if self.get_post_date(post_soup) > self.most_recent_post.date]

        self.add_posts_to_db(new_posts)

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.date = self.get_post_date(post_soup)
        new_post.title = post_soup.h4.text
        new_post.author = post_soup.find(class_='js-author').text
        new_post.url = self.ROOT_URL + post_soup.a['href']
        new_post.body = self.get_content(new_post.url)
        new_post.website = self.ROOT_URL
        new_post.name = 'Collaborative Fund'
        time.sleep(3)
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
    def get_image_src(img_tag) -> str:
        """Hopefully get a valid url for the picture to use as the src"""
        try:
            return CollaborativeScraper.ROOT_URL + img_tag['src']
        except:
            return ''

    @staticmethod
    def get_post_date(post_soup):
        """Give the post soup and return a datetime.date object witht he post date. If 
            you can't get the date for some reason or can't parse it then just return a date of 1/1/1
            so it will be obvious something is screwey if it gets into the db, but most likely will not 
            get in since it only pulls in new posts."""

        try:
            date_string = post_soup.time.text.strip()
            return parse(date_string).date()
        except:
            return datetime.date(1, 1, 1)

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
    def get_post_date(post_soup):
        """Give the post soup and return a datetime.date object witht he post date. If 
            you can't get the date for some reason or can't parse it then just return a date of 1/1/1
            so it will be obvious something is screwey if it gets into the db, but most likely will not 
            get in since it only pulls in new posts."""

        try:
            date_string = post_soup.find(class_='divDate').text.strip()
            return parse(date_string).date()
        except:
            return datetime.date(1, 1, 1)

    def is_in_db(self, post_soup):
        """Test if it is in the db by seeing if a post with that title is already in there somewhere."""
        post_title = self.get_title(post_soup)
        return post_is_in_db(value=post_title, filter_parameter='title')


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
                print(f'Something screwed up for post {index + 1} which is: {post_soup.find("h5")}')
            time.sleep(4)

        return posts


class AmnesiaScraper(SiteScrapper):
    """Inherits from . Implements specific functionality for scrapeing Aswath's website."""

    ROOT_URL = 'https://investoramnesia.com'
    BLOG_HOME = 'https://investoramnesia.com/category/sunday-reads'

    NAME = 'Amnesia'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object."""
        self.most_recent_post = self.most_recent_post = get_most_recent_post(self.NAME)

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        page_soup = sf.get_soup(self.BLOG_HOME)
        posts_on_page = page_soup.find_all(class_='post-content')
        new_posts = [self.build_post(post_soup) for post_soup in posts_on_page
                     if not self.is_in_db(post_soup)]

        self.add_posts_to_db(new_posts)

    def is_in_db(self, post_soup):
        """Test if it is in the db by seeing if a post with that url is already in there somewhere."""
        post_url = post_soup.a['href']
        return post_is_in_db(value=post_url, filter_parameter='url')


    def build_post(self, post_soup: BeautifulSoup) -> Posty:
        """Send in the soup of a post and spit out one of my post objects"""
        new_post = Posty()
        new_post.url = post_soup.a['href']

        page_soup = sf.get_soup(new_post.url)
        new_post.date = page_soup.find(class_='date').text.strip()
        new_post.title = page_soup.find(id='page-header-wrap').h1.text
        new_post.author = 'Jamie Catherwood'
        new_post.body = str(page_soup.find(class_='post-area'))
        new_post.website = self.ROOT_URL
        new_post.name = 'Amnesia'

        return new_post

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
                print(f'Something screwed up for post {index + 1}')
            time.sleep(3)

        return posts


class GatesScraper(SiteScrapper):
    ROOT_URL = 'https://www.gatesnotes.com'
    BLOG_HOME = 'https://www.gatesnotes.com/All'

    # Name should be same as name of posts.name that are created. This is used for sql queries later.
    NAME = 'Gates Notes'

    def __init__(self):
        """Only thing this does, is to populate the most_recent_post variable which contains a models.Post object.
            and get the chrome driver up and running.
        """
        self.most_recent_post = get_most_recent_post(self.NAME)
        # Declaring it up here so that all methods can use the chrome driver after it has been created.
        self.driver = sf.get_chrome_driver()

    def get_new_posts(self):
        """Check the front page for any new posts and download those if they are newer than the newest in the db."""

        self.driver.get(self.BLOG_HOME)
        time.sleep(4)  # Sleep to make sure the page is fully loaded.
        page_soup = BeautifulSoup(self.driver.page_source)
        posts_on_page = page_soup.find_all(class_='TGN_site_ArticleItemSearchThumb')
        new_posts = [self.build_post(post_soup) for post_soup in posts_on_page
                     if not self.is_in_db(post_soup)]

        self.add_posts_to_db(new_posts)

    def is_in_db(self, post_soup):
        """Test if it is in the db by seeing if a post with that url is already in there somewhere."""
        post_url = self.ROOT_URL + post_soup.a['href']
        return post_is_in_db(value=post_url, filter_parameter='url')

    def build_post(self, post_soup):
        """Send in the soup of a post and spit out one of my post objects"""

        new_post = Posty()
        new_post.url = self.ROOT_URL + post_soup.a['href']

        self.driver.get(new_post.url)
        page_soup = BeautifulSoup(self.driver.page_source)

        new_post.date = page_soup.find(class_='article_top_dateline').text
        new_post.title = page_soup.find(class_='article_top_head').text
        new_post.author = 'Bill Gates'

        new_post.body = str(page_soup.find(class_='TGN_site_Articlecollumn'))
        new_post.website = self.ROOT_URL
        new_post.name = 'Gates Notes'
        time.sleep(1)

        return new_post

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
                print(f'Something screwed up for post {index + 1}')
            time.sleep(3)

        return posts


def get_most_recent_post(blog_name: str = None) -> Posty:
    """Get the most recent post. Filtered by the name if one is passed in."""

    api_root = WEB_ROOT + 'api/blog-external-list/most-recent/'
    if blog_name:
        url = f'{api_root}?name={blog_name}'
    else:
        url = api_root

    response = requests.get(url)
    return Posty(response.text)


def post_is_in_db(value: str, filter_parameter: str) -> bool:
    """Test whether the post is in the db using either. I should update this to include the ability to filter by blog
     name as well."""

    url = WEB_ROOT + 'api/blog-external-list/'
    if filter_parameter == 'url':
        url = f'{url}?url={value}'
    elif filter_parameter == 'title':
        url = f'{url}?title={value}'

    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False
