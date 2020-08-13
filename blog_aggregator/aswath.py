import os
from docx import Document
import re
import sys
import datetime
sys.path.append('C:/Users/15314/source/repos/WebScraping/Scrapers')
import scrapfunctions as scrappy
import urllib
import bs4

# YEARS = [str(2008 + i) for i in range(12)]
# MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

IMAGE_FOLDER_PATH = r'C:\Users\15314\source\repos\WebScraping\blog_aggregator\images'

YEARS = ['2015']
MONTHS = ['12']

invalid_urls = []
all_posts = []

#@scrappy.time_usage
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
    new_post.body = get_post_body(post_soup, new_post)

    return new_post



def get_post_body(post):
    """Get the post body including images given the soup. Returns as a list."""
    
    # list containing tuples that have the type of content at index 0 and content at index 2
    all_text = []

    # Go through all of children and append all navigable strings and image src urls
    # Also append their bs4 types as first index of tuple.
    all_body_children = post.find(class_='post-body').descendants
    
    for child in all_body_children:
        if type(child) is bs4.element.NavigableString:
            all_text.append((type(child), child))
        elif type(child) is bs4.element.Tag:
            if child.name == 'img':
                if child['src'] is not None:
                    img_url = child['src']
                    all_text.append((type(child),img_url))
                    save_image(img_url)
                   

    return all_text


def save_image(image_url):
    """Save a blog image in the folder"""
    base_name = image_url.split('/')[-1]
    with open(IMAGE_FOLDER_PATH + '\\' + base_name, 'wb') as imagefile:
        imagefile.write(urllib.request.urlopen(image_url).read())



class Post():
    date = ''
    title = ''
    # Body is a touple
    body = []

    def convert_date(self):
        """Try to convert the text date to datetime, but if it does not work then keep it
        as a string"""
        # This is sketch. I should not allow the possibility for self.date to be two different types.
        try:
            self.date = datetime.datetime.strptime(self.date, '%A, %B %d, %Y')
        except:
            pass

    def __str__(self):
        return str(f'{self.date}\n{self.title}\n{self.body}')


if __name__ == "__main__":    

    try:
        main()
    except:
        print('Welp. Something screwed up somewhere so that is a bummer huh!?')
    else:
        print('Done!')
        
        with open('texty.html', 'w') as f:
            for post in all_posts:
                post.convert_date()
                f.write('<p>' + str(post.body) + '<p>')
                