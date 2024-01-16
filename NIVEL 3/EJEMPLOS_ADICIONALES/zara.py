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
import re
from datetime import date
import requests          ##para descargar una imagen 
from PIL import Image    ##para convertir 0 y 1 a imagen
import io  
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
import numpy as np
 
opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("disable-infobars")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36")
# opts.add_argument("download.default_directory=C:/Downloads")
# instalando del driver de selenium que va a controlar nuestro navegador
# a partir de este objeto voy a crear web scraping e interacciones
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
 
# voy a la pagina que requiero Y SACO LOS LINK DE LAS PÁGINAS
#######################################################################################################################
#######################################################################################################################
driver.get('https://www.zara.com/es/es/mujer-zapatos-tacon-l1271.html?v1=1549161')
time.sleep(2)
productos = driver.find_elements_by_xpath('/html/body/div[3]/section/div/section/div/ul/li')
    ##// para que nos busque en todos los hijos de la raiz en raiz
porfolios = []

for producto in productos:
  
    familia_subfamilia = driver.current_url
  
    marca = "Na"
    
    empresa = "zara"
    try:
        descripcion = producto.find_element_by_xpath('.//div/div/a[@class="name _item"]').text
        print(descripcion) 
    except (ElementNotVisibleException, NoSuchElementException) as e:    
        print(e)   
      ## . para que nos busque en los hijos de del elemento productos // para que haga la busqueda
    
    try:
        precio_activo = producto.find_element_by_xpath('.//div/div/div/span[contains(@class,"main-price")]').text
        print(precio_activo)
    except (ElementNotVisibleException, NoSuchElementException) as e:    
          print(e)
  
    # pvp = producto.find_element_by_xpath('.//s[contains(@class,"rd__productinfo__sale-price")]').text

    porfolios.append({
          "fecha_extracion":date.today(),
          "empresa":empresa,
          "familia_subfamilia":familia_subfamilia,                        
          "marca":marca,
          "descripcion":  descripcion,
          "precio_venta": precio_activo
          # "pvp_regular":pvp
      })
    
    try:
        url = producto.find_element_by_xpath('.//a/div/img')
        # HAGO QUE EL NAVEGADOR HAGA SCROLLING HASTA ESE ELEMENTO
        # PARA QUE CARGUE LA IMAGEN
        driver.execute_script("arguments[0].scrollIntoView(true);", url);
        sleep(0.5) # ESPERO A QUE LA IMAGEN CARGUE
        # VUELVO A OBTENER EL ELEMENTO PARA OBTENER YA EL SRC CARGADO
        url = producto.find_element_by_xpath('.//a/div/img')
        # obtengo el URl de la imagen del anuncio
        url = url.get_attribute('src')

        print (url)
        
        # con requests, hago el requerimiento a la URL de la imagen
        image_content = requests.get(url).content

        # PROCESAMIENTO DE LA IMAGEN
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = './imagenes/'+empresa+'_'+descripcion +'.jpg'  # nombre a guardar de la imagen
        with open(file_path, 'wb') as f:
            image.save(f, "JPEG", quality=60)
    except Exception as e:
      print(e)
      print ("Error")

driver.close()
df = pd.DataFrame(porfolios)
print(df)