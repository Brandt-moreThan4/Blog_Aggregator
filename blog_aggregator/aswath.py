import os
import re
import sys
import datetime
sys.path.append('C:/Users/15314/source/repos/WebScraping/Scrapers')
import scrapfunctions as scrappy
import urllib
import bs4
import string
# from docx import Document
# from docx.shared import Inches

# YEARS = [str(2008 + i) for i in range(12)]
# MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

IMAGE_FOLDER_PATH = r'C:\Users\15314\source\repos\WebScraping\blog_aggregator\images'

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
            # child.strip())
            all_content.append(('NavigableString', child))
        elif isinstance(child, bs4.element.Tag):
            if child.name == 'img':
                if child['src'] is not None:
                    source_img_url = get_img_url(child)
                    destination_path = IMAGE_FOLDER_PATH + '\\' + format_filename(new_post.title.strip())  
                    destination_path += '--' + source_img_url.split('/')[-1]
                    save_image(source_img_url, destination_path)
                    all_content.append(('image',destination_path))
                    
                
    return all_content


def get_img_url(img_tag):
    """Given an image tag, get the url where that image is stored"""

    # First try to get the big image from the <a> tag, but if that doesn't work then just go for the src image url
    try:
        return img_tag.parent['href']
    except:
        return img_tag['src']



def save_image(source_img_url, destination_path):
    """Save a blog image in the folder"""
    
    try:
        with open(destination_path, 'wb') as imagefile:
            imagefile.write(urllib.request.urlopen(source_img_url).read())
    except:
        pass


def make_word_doc():
    """Make a word doc from the post objects"""
    
    doc = Document()
    for post in all_posts:
        doc.add_paragraph('\n\n----NEW POSTTTTT---\n\n')
        doc.add_paragraph(post.title + '\n')
        doc.add_paragraph(str(post.date) + '\n')
        chunks  = []
        for typey, content in post.body:
            if typey == 'image':
                doc.add_paragraph(''.join(chunks))
                chunks = []
                doc.add_picture(content, width=Inches(6.5))
            else:
                chunks.append(content)
        if chunks:
            doc.add_paragraph(''.join(chunks))
        
        doc.add_paragraph('\n\n-------END POST------\n\n\n\n\n\n')
    
    doc.save('aswath.docx')


def make_html():
    with open('test_aswath.html', 'w') as f:
        # f.write('<style>* {with:<style>')
        for post in all_posts:
            f.write('<div>----NEW POSTTTTT---</div>')
            f.write(f'<div>----{post.title}---</div>')
            f.write(f'<div>----{post.date}---</div>')
            
            chunks  = []
            for typey, content in post.body:
                if typey == 'image':
                    f.write(f"<pre>{''.join(chunks)}</pre>")
                    chunks = []
                    f.write(f'<img src="{content}"></img>')
                else:
                    chunks.append(content)
            if chunks:
                f.write(f"<pre>{''.join(chunks)}</pre>")
            f.write(f"<div>-------END POST------</div>")


def format_filename(s):
    """Take a string and return a valid filename constructed from the string.
Uses a whitelist approach: any characters not present in valid_chars are
removed. Also spaces are replaced with underscores.
"""
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


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

    
    main()

    print('Done!')
        
        # with open('texty.html', 'w') as f:
        #     for post in all_posts:
        #         post.convert_date()
        #         f.write('<p>' + str(post.body) + '<p>')
                