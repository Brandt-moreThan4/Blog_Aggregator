import time
from pathlib import Path

from bs4 import BeautifulSoup
from django.template.loader import get_template

import scrapfunctions as scrappy
from post_classes import Post
import temp_setup

driver = scrappy.get_chrome_driver()
ROOT_URL = 'https://www.gatesnotes.com'


@scrappy.time_usage
def main():
    BLOG_ARCHIVE = 'https://www.gatesnotes.com/All'
    driver.get(BLOG_ARCHIVE)
    time.sleep(3)
    archive_page = BeautifulSoup(driver.page_source)

    while True:
        post_on_page = archive_page.find_all(class_='TGN_site_ArticleItemSearchThumb')
        # Above does not work for some reason
        posts = []
        for post_soup in post_on_page:
            posts.append(build_post(post_soup))
            time.sleep(2)

        make_html({'posts': posts})
        break


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.url = ROOT_URL + post_soup.a['href']
    driver.get(new_post.url)
    page_soup = BeautifulSoup(driver.page_source)
    new_post.title = page_soup.find(class_='article_top_head').text
    new_post.date = page_soup.find(class_='article_top_dateline').text
    new_post.author = 'Bill Gates'
    new_post.body = str(page_soup.find(class_='TGN_site_Articlecollumn'))

    return new_post


def make_html(context):
    post_as_html = get_template("gates.html").render(context)
    gates_folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\gates_posts')
    file_stem = 'lol.html'
    post_file = gates_folder / file_stem

    with post_file.open('w', encoding='utf-8') as f:
        f.write(post_as_html)


if __name__ == "__main__":
    main()
