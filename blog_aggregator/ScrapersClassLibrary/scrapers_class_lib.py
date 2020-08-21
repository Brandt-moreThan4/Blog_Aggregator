"""Library of all the scraping classes"""
import datetime
import sqlite3

from django.template.loader import get_template
import temp_setup
from pathlib import Path


class SiteScraper:
    """Generic scraper with properties that all scrapers should have."""
    ROOT_URL = None
    BLOG_HOME = None

    @staticmethod
    def add_posts_to_db(posts):
        """Give a list of Post objects and add each to the db."""
        conn = sqlite3.connect('scrapey.db')
        cur = conn.cursor()

        for post in posts:
            cur.execute("""INSERT INTO Scrape_Posts (date, title, author, body, url, website, name) 
                       VALUES(?, ?, ?, ?, ?, ?, ?);""",
                        [post.date, post.title, post.author, post.body, post.url, post.website,
                         post.name])

        conn.commit()
        conn.close()

    @staticmethod
    def make_html(name: str, folder_name: str, template_name: str):
        conn = sqlite3.connect('scrapey.db')
        cur = conn.cursor()
        query = cur.execute("""SELECT * FROM Scrape_Posts WHERE name=? LIMIT 3""", [name])
        posts = []
        for row in query:
            post = Post()
            post.body = row[4]
            post.title = row[2]
            posts.append(post)

        posts_as_html = get_template(template_name + ".html").render({'posts': posts})
        folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator') / folder_name
        with (folder / 'lol.html').open('w',  encoding='utf-8') as f:
            f.write(posts_as_html)


class Post:
    date = ''
    title = ''
    author = ''
    body = ''
    url = ''
    website = ''
    name = ''

    # @property
    # def date(self):
    #     # Should return as a string?
    #     return self._date
    #
    # @property.setter
    # def date(self, value):
    #     """Try to convert the text date to datetime, but if it does not work then keep it
    #     as a string"""
    #     # This is sketch. I should not allow the possibility for self.date to be two different types.
    #     try:
    #         # Try a bunch of different converts?
    #         self._date = datetime.datetime.strptime(self.date, '%A, %B %d, %Y')
    #     except:
    #         # If convert doesn't work then just leave it as is.
    #         pass

    # def __str__(self):
    #     return str(f'{self.date}\n{self.title}\n{self.body}')
