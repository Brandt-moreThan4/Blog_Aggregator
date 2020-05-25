from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup
import scrapfunctions as sp

title = sp.get_h1('https://www.programiz.com/python-programming/exception-handling')

print(title)