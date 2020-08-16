import re
import sys
import time

sys.path.append(r'C:\Users\15314\PycharmProjects\WebScraping\Scrapers')
import scrapfunctions as scrappy
import bs4
from pathlib import Path
from post_classes import Post
import temp_setup
from django.template.loader import get_template

# YEARS = [str(2008 + i) for i in range(12)]
MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

YEARS = ['2015']
# MONTHS = ['12']

invalid_urls = []
all_posts = []


@scrappy.time_usage
def main():
    # Go year by year and then month by month and extract all blog content on those pages.
    for year in YEARS:
        for month in MONTHS:
            url = 'http://aswathdamodaran.blogspot.com/' + year + '/' + month
            page_soup = scrappy.get_soup(url)

            if page_is_valid(page_soup):
                extract_posts(page_soup)
            else:
                invalid_urls.append(url)

            global all_posts
            make_html({'posts': all_posts}, year, month)

            all_posts = []
            time.sleep(1)


def page_is_valid(page_soup):
    """Give the whole soup on the page and returns True if it contains at least one valid post."""

    post = page_soup.find(class_='post-body')
    return post is not None


def extract_posts(page_soup):
    """lol """
    posts = page_soup.find_all(class_='post-outer')

    for post_soup in posts:
        new_post = build_post(post_soup)
        all_posts.append(new_post)


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.title = post_soup.find(class_='post-title').text
    new_post.date = post_soup.parent.parent.find(class_='date-header').text
    new_post.body = str(post_soup)

    return new_post


def make_html(context, year, month):
    posts_as_html = get_template("aswath.html").render(context)

    year_dir = Path(r'C:\Users\15314\source\repos\WebScraping\blog_aggregator\aswath_posts') / year
    if not year_dir.exists():
        year_dir.mkdir()

    with (year_dir / (month + '.html')).open('w') as f:
        f.write(posts_as_html)


if __name__ == "__main__":
    main()
