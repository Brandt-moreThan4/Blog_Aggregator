from bs4 import BeautifulSoup
import requests
from selenium import webdriver


def get_soup(url):
    """Returns beautiful Soup object of the requested page"""
    try:
        page_response = requests.get(url)
    except:
        print('Error loading url')
        return None

    try:
        soup = BeautifulSoup(page_response.text, 'html5lib')
    except:
        print('Trouble parsing the soup for: {}'.format(url))
        return None
    else:
        return soup


def get_chrome_driver():
    """Returns a selenium driver object to manipulate chrome"""

    driver_path = r'C:\Users\bgreen3\Desktop\chromedriver'
    try:
        driver = webdriver.Chrome(driver_path)
    except:
        print('Something screwed up getting the driver. Make sure chrome is downloaded and the path is correct')
        return None
    else:
        return driver
