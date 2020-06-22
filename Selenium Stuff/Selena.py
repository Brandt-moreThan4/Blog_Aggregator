from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import requests
import os


def main():
    # website_path = "https://www.oaktreecapital.com/insights/howard-marks-memos"
    # website_path = "https://funwithbrandt.azurewebsites.net/KnowledgeRepository"
    website_path = "https://www.oaktreecapital.com/insights/howard-marks-memos"
    # website_path = "https://funwithbrandt.azurewebsites.net/KnowledgeRepository"
    # driver = get_chrome_driver()
    # driver.get(website_path)
    # soup = BeautifulSoup(driver.page_source)
    # search_box = driver.find_element_by_id('searchBox')
    # search_box.send_keys("Python")
    # el = driver.find_elements(By.TAG_NAME, value='button')
    # el[1].submit()
    # print('lol')
    print(soup.prettify())


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


if __name__ == '__main__':
    # main()

    website_path = "https://www.oaktreecapital.com/insights/howard-marks-memos"
    driver = get_chrome_driver()

    driver.get(website_path)
    soup = BeautifulSoup(driver.page_source)
    pdf_link = driver.find_element_by_link_text('Uncertainty II')
    driver.execute_script("window.scrollBy(0, 800);")
    pdf_link.click()
    for handle in driver.window_handles:
        driver._switch_to.window(handle)
        print(handle)
