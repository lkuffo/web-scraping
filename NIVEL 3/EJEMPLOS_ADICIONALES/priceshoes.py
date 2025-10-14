from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import random
from time import sleep
from selenium import webdriver # pip install selenium
 
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
 
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get('https://www.priceshoes.com/productos/marcas/adidas')

while True:
    # Esperamos un poco a que cargue bien la informacion de la lista inicial.
    sleep(2)
    #todos los productos en una lista
    link_productos = driver.find_elements_by_xpath('//a[@class="product-item-link"]')
    links_de_pagina = []
    for tag_a in link_productos:
        links_de_pagina.append(tag_a.get_attribute("href"))
 
    for link in links_de_pagina:
        print(link)
        try:
            driver.get(link)
            sleep(4) # Esperamos que carguen las tallas
            _id = driver.find_element_by_xpath('//div[@itemprop="sku"]').text
            print(_id)

            # XPATH para seleccionar todas las opciones del combobox
            tallas = driver.find_elements_by_xpath('//select[contains(@class, "swatch-select talla_")]//option')
            for talla in tallas:
                n_tallas = talla.text
                print(n_tallas)

            driver.back() # luego de obtener toda la info recien iremos hacia atras
        except Exception as e:
            print(e)
            driver.back() # Si sucede algun error, tambien vamos para atras.
 
    try:
      boton_siguiente = driver.find_element_by_xpath('//li[@class="item pages-item-next"]/a')
      boton_siguiente.click()
    except Exception as e:
      print (e)
      break