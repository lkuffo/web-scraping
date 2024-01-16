import time
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver  ## pip install selenium # driver capturador de info en la web
from selenium.webdriver.chrome.options import Options  ## para enmascarar al robot
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
import pandas as pd
 
opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("disable-infobars")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36")
 
# instalando del driver de selenium que va a controlar nuestro navegador
# a partir de este objeto voy a crear web scraping e interacciones
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
# voy a la pagina que requiero
driver.get('https://douglas.es/c/perfumes/')
 

porfolios = []
#max_pag = 0
while True:
  #todos los productos en una lista
  productos = driver.find_elements_by_xpath('//div[@class="rd__product-tile sd__product-tile"]')
  ##// para que nos busque en todos los hijos de la raiz en raiz

  for producto in productos:
      descripcion = producto.find_element_by_xpath('.//a[@class="rd__copytext rd__copytext--90 rd__bb-productinfo__name rd__item-basketflyout__copytext"]').text
      print(descripcion)  ## . para que nos busque en los hijos de del elemento productos // para que haga la busqueda
 
      precio_activo = producto.find_element_by_xpath('.//span[contains(@class,"rd__productinfo__price--sale")]').text
      print(precio_activo)
 
 
      porfolios.append({
        "descripcion": descripcion,
        "precio_venta": precio_activo
      })
  #max_pag += 1
  
  #if (max_pag == 3): break
 
  try:
      driver.execute_script("return arguments[0].scrollIntoView(true);", WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, '//a[contains(@class,"rd__pagination__next")]'))))
      driver.find_element_by_xpath('//a[contains(@class,"rd__pagination__next")]').click()
      print("Navigating to Next Page")
  except (TimeoutException, WebDriverException) as e:
      print (e)
      print("Last page reached")
      break
 
df = pd.DataFrame(porfolios)
print(df)
df.to_csv("pruebadataframe.csv")