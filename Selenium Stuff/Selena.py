from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
import os


def get_chrome_driver():
    """Returns a selenium driver object to manipulate chrome"""

    driver_path = r'C:\Users\15314\source\repos\WebScraping\chromedriver.exe'
    options = webdriver.chrome.options.Options()
    options.set_headless(headless=True)
    try:
        driver = webdriver.Chrome(driver_path, options = options)
    except:
        print('Something screwed up getting the driver. Make sure chrome is downloaded and the path is correct')
        return None
    else:
        return driver


if __name__ == '__main__':

    website_path = "https://www.collaborativefund.com/blog/archive/"
    driver = get_chrome_driver()

    driver.get(website_path)
    soup = BeautifulSoup(driver.page_source)
    print(soup.prettify())