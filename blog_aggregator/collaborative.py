import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup
from django.template.loader import get_template

# sys.path.append(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\Scrapers')
import scrapfunctions as scrappy
from post_classes import Post
import temp_setup

driver = scrappy.get_chrome_driver()
ROOT_URL = 'https://www.collaborativefund.com'
all_the_posts = []


@scrappy.time_usage
def main():
    BLOG_ARCHIVE = 'https://www.collaborativefund.com/blog/archive/'

    driver.get(BLOG_ARCHIVE)
    soup = BeautifulSoup(driver.page_source)

    all_posts = soup.find_all(class_='post-item')
    for post in all_posts:
        new_post = build_post(post)
        all_the_posts.append(new_post)
        make_html({'posts': [new_post]}, new_post)
        time.sleep(5)


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.title = post_soup.h4.text
    new_post.date = post_soup.time.text
    new_post.author = post_soup.find(class_='js-author').text
    new_post.body = get_content(post_soup)

    return new_post


def get_content(post_soup):
    post_url = ROOT_URL + post_soup.a['href']
    driver.get(post_url)
    page_soup = BeautifulSoup(driver.page_source)
    clean_images(page_soup.article)
    return str(page_soup.article)


def clean_images(post_soup):
    images = post_soup.find_all('img')
    for image in images:
        image.attrs = {'src': get_image_src(image), 'alt': 'Sorry Brandt screwed up this image somehow.',
                       'class': 'img-fluid'}


def get_image_src(img_tag):
    """Hopefully get a valid url for the picture to use as the src"""
    try:
        return ROOT_URL + img_tag['src']
    except:
        return ''


def make_html(context, post):
    post_as_html = get_template("collab.html").render(context)
    collab_folder = Path(r'C:\Users\15314\PycharmProjects\Blog_Aggregator\blog_aggregator\collaborative_posts')
    file_stem = scrappy.format_filename(str(post.date) + post.title + '.html')
    post_file = collab_folder / file_stem

    with post_file.open('w', encoding='utf-8') as f:
        f.write(post_as_html)


if __name__ == "__main__":
    main()
