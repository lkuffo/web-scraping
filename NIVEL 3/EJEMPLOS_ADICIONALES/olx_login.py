import random
from time import sleep
from selenium import webdriver
import pandas as pd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
)
 
driver = webdriver.Chrome('./chromedriver')
driver.get('https://www.olx.com.ec/items/q-casas-venta')
 
user = 'USERNAME'
password = 'PASSWORD'
# BOTON DE LOGIN
ingreso = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLogin"]'))
)
ingreso.click()

# BOTON DE EMAIL LOGIN 
tp = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="emailLogin"]'))
)
tp.click()

# ESCRIBIENDO EL EMAIL
input_user = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))
)
input_user.send_keys(user)

# CLICK EN BOTON SIGUIENTE
btsiguiente = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]/span'))
)
btsiguiente.click()

# ESCRIBIENDO EL PASSWORD
input_pass = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
)
input_pass.send_keys(password)

# CLICK EN BOTON INGRESAR
btsiguiente = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]/span'))
)
btsiguiente.click()

 
sleep(3)
boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
 
for i in range(2):
    try:
        boton.click()
        sleep(random.uniform(3.0, 8.0))
        boton = driver.find_element_by_xpath('//button[@data-aut-id="btnLoadMore"]')
    except:
        break
autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')
data = []
for auto in autos:
    precio = auto.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    data.append({'precio': precio, 'descripcion': descripcion})
 
df = pd.DataFrame(data)
print(df)
df.to_csv('casas.csv', index=True)