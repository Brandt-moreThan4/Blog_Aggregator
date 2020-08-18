import time
from pathlib import Path

from bs4 import BeautifulSoup
from django.template.loader import get_template

import scrapefunctions as scrappy
from post_classes import Post
import temp_setup

driver = scrappy.get_chrome_driver()
ROOT_URL = 'https://www.collaborativefund.com'


# print('lol')

@scrappy.time_usage
def main():
    BLOG_ARCHIVE = 'https://stratechery.com/category/articles/'
    driver.get(BLOG_ARCHIVE)
    archive_page = BeautifulSoup(driver.page_source)

    while True:
        post_on_page = archive_page.find_all('article')
        posts = []
        for post_soup in post_on_page:
            posts.append(build_post(post_soup))
            time.sleep(2)

        make_html({'posts': posts})
        break


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.title = post_soup.h1.text
    new_post.date = post_soup.time.text
    new_post.author = 'Ben Thompson'
    new_post.url = post_soup.a['href']
    new_post.body = get_content(new_post.url)

    return new_post


def get_content(post_url):
    driver.get(post_url)
    page_soup = BeautifulSoup(driver.page_source)

    return str(page_soup.article)



def make_html(context):
    post_as_html = get_template("stratechery.html").render(context)
    collab_folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\stratechery_posts')
    file_stem = 'lol.html'
    # file_stem = scrappy.format_filename(str(post.date) + post.title + '.html')
    post_file = collab_folder / file_stem

    with post_file.open('w', encoding='utf-8') as f:
        f.write(post_as_html)


if __name__ == "__main__":
    main()
