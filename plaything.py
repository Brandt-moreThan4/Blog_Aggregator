from bs4 import BeautifulSoup
import scrapfunctions as sp
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# os.startfile(r'C:\Users\bgreen3\Desktop\temp.txt')
if __name__ == '__main__':

    website_path = "https://www.oaktreecapital.com/insights/howard-marks-memos"
    response = requests.get('https://www.oaktreecapital.com/docs/default-source/memos/uncertainty-ii.pdf')
    soup = sp.get_soup(url=website_path)
    all_tables = soup.find_all('table')
    memo = soup.find(id='tvMemoArchivet7')
