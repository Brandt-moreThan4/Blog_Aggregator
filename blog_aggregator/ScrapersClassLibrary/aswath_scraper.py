"""Aswath scraper"""

import time
from pathlib import Path
import sqlite3
import temp_setup

from django.template.loader import get_template
from ScrapersClassLibrary.scrapers_class_lib import SiteScraper, Post
import scrapefunctions as sf



class AswathScraper(SiteScraper):
    """Inherits from SiteScraper. Implements specific functionality for scrapeing Aswath's website."""
    ROOT_URL = 'http://aswathdamodaran.blogspot.com'
    BLOG_HOME = 'http://aswathdamodaran.blogspot.com'

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
                #time.sleep(1)
        # self.make_html()

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
        new_post.date = post_soup.parent.parent.find(class_='date-header').text
        new_post.title = post_soup.find(class_='post-title').text
        new_post.author = 'Aswath Damodaron'
        new_post.body = new_post.body = str(post_soup)
        new_post.url = post_soup.find(class_='post-title').a.get('href')
        new_post.website = self.ROOT_URL

        return new_post

    @staticmethod
    def add_posts_to_db(posts):
        """Give a list of Post objects and add each to the db."""
        conn = sqlite3.connect('scrapey.db')
        cur = conn.cursor()

        for post in posts:
            cur.execute("""INSERT INTO Scrape_Posts (date, title, author, body, url, website) 
               VALUES(?, ?, ?, ?, ?, ?);""", [post.date, post.title, post.author, post.body, post.url, post.website])

        conn.commit()
        conn.close()

    # def make_html(self):
    #
    #     conn = sqlite3.connect('scrapey.db')
    #     cur = conn.cursor()
    #     query = cur.execute("""SELECT * FROM Scrape_Posts""")
    #     posts = []
    #     for row in query:
    #         print(row)
    #         post = Post()
    #         post.body = row[4]
    #         posts.append(post)
    #
    #     posts_as_html = get_template("aswath.html").render({'posts': posts})
    #
    #     folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\aswath_posts')
    #
    #     with (folder / 'lol.html').open('w') as f:
    #         f.write(posts_as_html)


if __name__ == '__main__':
    test = AswathScraper()
    test.make_html()
    # test.get_historical_posts()