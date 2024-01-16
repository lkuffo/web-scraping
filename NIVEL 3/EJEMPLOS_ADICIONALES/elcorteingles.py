import requests

from PIL import Image

import io



from selenium import webdriver

from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options



import time

import random



opts = Options()

opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36")

driver = webdriver.Chrome('./chromedriver', options=opts)



driver.get('https://www.elcorteingles.es/supermercado/alimentacion-general/')

time.sleep(10)

links_categorias = driver.find_elements(By.XPATH, '//a[@class="link _primary _level3 tree-link   "]')

links_categorias_pagina = []

for link_categoria in links_categorias:

    links_categorias_pagina.append(link_categoria.get_attribute("href"))

    for categoria in links_categorias_pagina:

        while True:

            links_productos = driver.find_elements(By.XPATH, '//a[@class="event js-product-link"]')

            links_de_la_pagina = []

            for a_link in links_productos:

                links_de_la_pagina.append(a_link.get_attribute("href"))



            for link in links_de_la_pagina:

                try:

                    driver.get(link)

                    titulo = driver.find_element(By.XPATH, '//span[@itemprop="name"]').text

                    precio = driver.find_element(By.XPATH, '//div[@class="prices pdp-prices"]').text

                    descripcion = driver.find_element(By.XPATH, '//div[@class="pdp-info-container"]').text



                    print (titulo)

                    print (precio)

                    print (descripcion)



                    driver.back()



                except Exception as e:

                    print (e)

                    driver.back()



           

            try:               

                puedo_seguir_horizontal = driver.find_element(By.XPATH, '//li[@id="pagination-next"]')

                puedo_seguir_horizontal.click()

            except:         

                break