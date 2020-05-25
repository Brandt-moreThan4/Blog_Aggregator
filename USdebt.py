from bs4 import BeautifulSoup
import scrapfunctions as sp
import csv
import os
import matplotlib.pyplot as plt
import numpy as np

debt_url = 'https://treasurydirect.gov/govt/reports/pd/histdebt/histdebt_histo5.htm'

debt_soup = sp.get_soup(debt_url)
debt_table = debt_soup.table
debt_rows = debt_table.find_all('tr')

file_name = 'debt.csv'
i = 0
if os.path.exists(file_name):
    while os.path.exists(file_name):
        i += 1
        file_name = 'debt' + str(i) + '.csv'

# Newline parameter set so that csv writer doesn't insert blank lines in between each row
with open(file_name, 'w+', newline='') as f:
    writer = csv.writer(f)
    csv_rows = []
    for row in debt_rows:
        csv_row = []
        c_row = row.find_all(['td', 'th'])
        for cell in c_row:
            csv_row.append(cell.get_text())

        # Just a check to make sure there is a date there. Since some were blank.
        if csv_row:
            if csv_row[0] != "":
                writer.writerow(csv_row)
                csv_rows.append(csv_row)


x_vals = []
y_vals = []

for i in range(1, len(csv_rows)-1):
    x_vals.append(csv_rows[i][0])
    y_vals.append(float(csv_rows[i][1].replace(',', '')))

x_vals.reverse()
y_vals.reverse()

fig, ax = plt.subplots()  # Create a figure containing a single axes.
plt.style.use('seaborn')
ax.plot(x_vals, y_vals, c='b')
plt.show()
