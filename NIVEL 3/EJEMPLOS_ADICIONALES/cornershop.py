import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
 
 
 
# User agent
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
 
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get('https://web.cornershopapp.com/store/9/search/toallitas%20humedas')  #https://web.cornershopapp.com/store/22/featured')
 
CP = '05130'
 
# iniciar hasta que aparezca el box de log in
loginlater = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//div[@class="user-close-modal-button"]/button'))
)
loginlater.click()
 
# ingresar el código postal
input_cp = WebDriverWait(driver, 10).until(
  EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Zip code"]'))
)
 
input_cp.send_keys(CP)
 
# dar clic a continuar
Continue = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (By.XPATH, '//button[@class="primary button"]'))
)
Continue.click()
 
sleep(random.uniform(5.0,6.0))
#departamentos = driver.find_elements_by_xpath('//div[@class="aisle-box card"]')
 
#for departamento in departamentos:
#    nombre_departamento = departamento.find_element_by_xpath('.//div[@class="card-header"]/h2/span').text
 
productos = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH,'//div[@class="product"]//div[@class="product-content"]/div[@class="product-info"]/h3'))
)
for producto in productos:
    #departamento = driver.find_element_by_xpath('.//ancestor::div[@class="card-header"]')
    #print(departamento.text)
    print(producto.text)
 
precios = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH,'//p[contains(@class, "price")]'))
)
for precio in precios:
    print(precio.text)
 
empaques = WebDriverWait(driver, 10).until(
EC.presence_of_all_elements_located((By.XPATH,'//p[contains(@class, "price")]/following-sibling::p'))
)
for empaque in empaques:
    print(empaque.text) 