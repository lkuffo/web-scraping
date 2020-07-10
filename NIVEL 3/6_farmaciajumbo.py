from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep

# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER


driver.get('https://www.jumbo.cl/despensa')

links_paginas = WebDriverWait(driver, 10).until(
  EC.presence_of_all_elements_located((By.XPATH, '//button[@class="page-number "]'))
)

links_paginacion = []
for tag_button in links_paginas:
  links_paginacion.append('https://www.jumbo.cl/despensa?page=' + tag_button.text)

for pagina in links_paginacion:
    print (pagina)
    driver.get(pagina)

    links_productos = WebDriverWait(driver, 10).until(
      EC.presence_of_all_elements_located((By.XPATH, '//a[@class="shelf-product-title"]'))
    )

    links_de_la_pagina=[]
    for tag_a in links_productos:
        links_de_la_pagina.append(tag_a.get_attribute("href"))

    for link in links_de_la_pagina[0: 1]:
        try:
            driver.get(link)
            nombre = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.XPATH, '//h1[@class="product-name"]'))
            ).text
            marca=driver.find_element_by_xpath('//span[@class="product-brand"]').text
            precio=driver.find_element(By.XPATH,'//div[@class="product-single-price-container"]').text
            print(nombre)
            print(marca)
            print(precio)
        
 
            driver.back()
        except Exception as e:
            print(e)
            driver.back()