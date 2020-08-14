import re
import sys
import datetime
sys.path.append('C:/Users/15314/source/repos/WebScraping/Scrapers')
import scrapfunctions as scrappy
import bs4
from pathlib import Path
from post_classes import Post, Image

# YEARS = [str(2008 + i) for i in range(12)]
# MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']


YEARS = ['2015']
MONTHS = ['12']

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
    
    # make_word_doc()
    make_html()


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



def get_post_body(post, new_post):
    """Get the post body including images given the soup. Returns as a list."""
    
    # list containing tuples that have the type of content at index 0 and content at index 2
    all_content = []

    # Go through all of children and append all navigable strings and image src urls
    # Also append their bs4 types as first index of tuple.
    all_body_children = post.find(class_='post-body').descendants

    for child in all_body_children:
        if isinstance(child, bs4.element.NavigableString):
            all_content.append(child)
        elif isinstance(child, bs4.element.Tag):
            if child.name == 'img':
                if 'src' in child.attrs:
                    image = Image(child, new_post)
                    all_content.append(image)
                    
    return all_content



def make_html():

    with (Path.cwd() / 'test_aswath.html').open('w') as f:
        for post in all_posts:
            f.write('<div>----NEW POSTTTTT---</div>')
            f.write(f'<div>----{post.title}---</div>')
            f.write(f'<div>----{post.date}---</div>')
            
            chunks  = []
            for content in post.body:
                if isinstance(content, Image):
                    all_chunk = ''.join(chunks)
                    all_chunk = all_chunk.replace('\n', '<br/>')
                    f.write(f"<div>{all_chunk}</div>")
                    chunks = []
                    f.write(f'<img src="{content.image_path}"></img>')
                else:
                    chunks.append(content)
            if chunks:
                f.write(f"<div>{''.join(chunks)}</div>")
            f.write(f"<div>-------END POST------</div>")




if __name__ == "__main__":    

    
    main()

    print('Done!')
        
        # with open('texty.html', 'w') as f:
        #     for post in all_posts:
        #         post.convert_date()
        #         f.write('<p>' + str(post.body) + '<p>')
                