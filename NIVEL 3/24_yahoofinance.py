import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#import chromedriver_binary
import string
pd.options.display.float_format = '{:.0f}'.format
 
 
# Set up Driver
is_link = 'https://finance.yahoo.com/quote/AAPL/financials?p=AAPL'
 
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

driver.get(is_link)
sleep(10)
html = driver.execute_script('return document.body.innerHTML;')
soup = BeautifulSoup(html,'lxml')
 
# Transferring this information into Python
close_price = [entry.text for entry in soup.find_all('span', {'class':'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'})]
 
features = soup.find_all('div', class_='D(tbr)')
 
headers = []
temp_list = []
label_list = []
final = []
index = 0
#create headers
for item in features[0].find_all('div', class_='D(ib)'):
    headers.append(item.text)
#statement contents
while index <= len(features)-1:
    #filter for each line of the statement
    temp = features[index].find_all('div', class_='D(tbc)')
    for line in temp:
        #each item adding to a temporary list
        temp_list.append(line.text)
    #temp_list added to final list
    final.append(temp_list)
    #clear temp_list
    temp_list = []
    index+=1
df = pd.DataFrame(final[1:])
df.columns = headers
 
 
# function to make all values numerical
def convert_to_numeric(column):
    first_col = [i.replace(',', '') for i in column]
    second_col = [i.replace('-', '') for i in first_col]
    final_col = pd.to_numeric(second_col)
 
    return final_col
 
 
for column in headers[1:]:
    df[column] = convert_to_numeric(df[column])
final_df = df.fillna('-')