from bs4 import BeautifulSoup
import requests
import time
import time
from pathlib import Path

if __name__ == '__main__':

    with (Path().cwd() / 'play_soup.html').open('r') as f:
        soup = BeautifulSoup(f.read())

    print(soup.prettify())

    lol = soup.img
    lol2 = soup.a
    lol3 = soup.p
    haha = soup.find('a')
    lol = soup.find_all('img')[1] 
    hehe = lol['src']
    hoho = lol.get('src')
    attr = lol.attr
