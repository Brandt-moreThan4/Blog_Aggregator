import time
from pathlib import Path

from bs4 import BeautifulSoup
from django.template.loader import get_template

import scrapefunctions as scrappy
from post_classes import Post
import temp_setup

ROOT_URL = 'https://investoramnesia.com'


@scrappy.time_usage
def main():
    BLOG_ARCHIVE = 'https://investoramnesia.com/category/sunday-reads/'

    archive_page = scrappy.get_soup(BLOG_ARCHIVE)
    post_on_page = archive_page.find_all(class_='post-content')
    posts = []

    # while archive_page.find('a', class_='Next') is not None:
    for post_soup in post_on_page:
        posts.append(build_post(post_soup))
        time.sleep(1)
        if len(posts) >= 3:
            break

    make_html({'posts': posts})


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.url = post_soup.a['href']
    page_soup = scrappy.get_soup(new_post.url)
    new_post.title = page_soup.find(id='page-header-wrap').h1.text
    new_post.date = page_soup.find(class_='date').text
    new_post.author = 'Jamie Catherwood'
    new_post.body = str(page_soup.find(class_='post-area'))

    return new_post


def make_html(context):
    post_as_html = get_template("osam.html").render(context)
    osam_folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\amnesia_posts')
    file_stem = 'lol.html'
    # file_stem = scrappy.format_filename(str(post.date) + post.title + '.html')
    post_file = osam_folder / file_stem

    with post_file.open('w', encoding='utf-8') as f:
        f.write(post_as_html)


if __name__ == "__main__":
    main()
