from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup as bs


def get_soup(url):
    """Returns beautiful Soup object of the requested page"""
    try:
        html = urlopen(url)
    except HTTPError as e:
        print('Error loading url')
        return None

    try:
        soup = bs(html, 'html5lib')
    except:
        print('Trouble parsing the soup for: {}'.format(url))
        return None
    else:
        return soup

