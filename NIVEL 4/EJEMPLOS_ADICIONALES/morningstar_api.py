from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import re
from datetime import date
 
headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36",
}
 
urlfinancials = 'http://financials.morningstar.com/finan/financials/getFinancePart.html?&callback=xxx&t=AAPL'
text_soup_financials = BeautifulSoup(json.loads(re.findall(r'xxx\((.*)\)', requests.get(urlfinancials, headers = headers).text)[0])['componentData'], 'lxml')
 
titlesfinancials = text_soup_financials.findAll('th', {'class': 'row_lbl'})
 
epslist = []
Grossincomelist = []
 
for title in titlesfinancials:
    if 'Cap Spending' in title.text:
        Grossincomelist = [td.text for td in title.findNextSiblings(attrs={'align': 'right'}) if td.text]
    if 'Earnings Per Share' in title.text:
        epslist = [td.text for td in title.findNextSiblings(attrs={'align': 'right'}) if td.text]

df = pd.DataFrame(
        {'Revenue': epslist,'Capex': Grossincomelist }, index=range(date.today().year - 11, date.today().year))

print(df)