from bs4 import BeautifulSoup
import scrapfunctions as sp
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np

debt_url = 'https://treasurydirect.gov/govt/reports/pd/histdebt/histdebt_histo5.htm'
debt_soup = sp.get_soup(debt_url)
debt_tbl = debt_soup.table # Debt table is only table on page
debt_tbl_rows = debt_tbl.find_all('tr')

dates, debt = [], []

for tbl_row in debt_tbl_rows:
    cells = tbl_row.find_all(['td', 'th'])
    if len(cells) > 0:
        if len(cells[0].get_text()) > 0:
            dates.append(cells[0].get_text())
            debt.append(cells[1].get_text())

# Delete headers and sort from oldest to newest and convert to date and float types
del dates[0]
del debt[0]
dates.reverse()
debt.reverse()
dates = [dt.datetime.strptime(date.replace(' ', ''),'%m/%d/%Y') for date in dates]
debt = [float(i.replace(',', '')) for i in debt]

numpy_ray = np.asarray([dates, debt])

fig, ax = plt.subplots()  # Create a figure containing a single axes.
plt.style.use('seaborn')
ax.plot(numpy_ray[0, :], numpy_ray[1, :], c='b')
plt.show()
