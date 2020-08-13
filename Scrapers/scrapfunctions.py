from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from docx import Document
import time

def get_soup(url):
    """Returns beautiful Soup object of the requested page or None if there was trouble somehwere along the way."""

    page_response = get_page_response(url)
    if page_response is not None:
        try:
            soup = BeautifulSoup(page_response.text)
        except:
            print('Trouble parsing the soup for: {}'.format(url))
            return None
        else:
            return soup
    else:
        print('The response object was "None" so there is no point in trying to parse')
        return None


def get_page_response(url):
    """Get a page response using the given url"""
    try:
        page_response = requests.get(url)
    except:
        print('Error loading url')
        return None
    else:
        return page_response


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


def time_usage(func):
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        retval = func(*args, **kwargs)
        end_time = time.time()
        print(f"elapsed time: {(end_time - begin_time)}")
        return retval
    return wrapper


def convert_txt_to_word(text, destination_path='Federalist Papers.docx'):
    """Takes text string and saves it as a word document"""
    doc = Document()
    doc.add_paragraph(text)
    doc.save(destination_path)