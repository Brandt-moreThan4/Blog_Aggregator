import re
import sys
import time
sys.path.append('C:/Users/15314/source/repos/WebScraping/Scrapers')
import scrapfunctions as scrappy
import bs4
from pathlib import Path
from post_classes import Post
import temp_setup
from django.template.loader import get_template


invalid_urls = []
all_posts = []

@scrappy.time_usage
def main():


    ROOT_URL = 'https://www.eugenewei.com'
    current_url = ROOT_URL

    counter = 1
    while True:
        print(f'post: {counter}')
        print(f'Getting soup for {current_url}')
        time.sleep(15)   

        page_soup = scrappy.get_soup(current_url)
        posts_on_page = [build_post(post_soup) for post_soup in page_soup.find_all(class_='post')]
        make_html({'posts':posts_on_page}, counter)

        try:
            current_url = ROOT_URL + page_soup.find(id='nextLink')['href']
        except:
            current_url = None
 
        counter += 1        
        #if current_url is None:
        if counter == 4:
            break
    


def build_post(post_soup):
    """Send in the soup of a post and spit out one of my post objects"""
    new_post = Post()
    new_post.title = post_soup.header.h1.text
    new_post.date = post_soup.footer.find(class_='date').text
    clean_images(post_soup)
    # still need to correct side notes. Probably just delete them?
    new_post.body = str(post_soup)

    return new_post


def clean_images(post_soup):

    images = post_soup.find_all('img')
    for image in images:
        image.attrs = {'src':get_image_src(image), 'alt':'Sorry Brandt screwed up this image somehow.', 'class':'img-fluid'}
        image.parent.attrs = {'style': 'max-width:700px;'}


def get_image_src(img_tag):
    """Hopefully get a valid url for the picture to use as the src"""
    if img_tag.get('src') is not None:
        return img_tag['src']
    elif img_tag.get('data-src') is not None:
        return img_tag['data-src']
    elif img_tag.get('data-image') is not None:
        return img_tag['data-image']
    else:
        return ''



def make_html(context, counter):

    posts_as_html = get_template("eugene.html").render(context)
    eugene_folder = Path(r'C:\Users\15314\source\repos\WebScraping\blog_aggregator\eugene_posts')
    post_file = eugene_folder / f'Page {counter}.html'
    with (post_file).open('w', encoding='utf-8') as f:
        f.write(posts_as_html)



if __name__ == "__main__":    

    main()

                