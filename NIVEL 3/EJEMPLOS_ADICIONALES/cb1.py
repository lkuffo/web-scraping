import time
from time import sleep
from selenium import webdriver  ## pip install selenium # driver capturador de info en la web
from selenium.webdriver.chrome.options import Options  ## para enmascarar al robot
import pandas as pd
from datetime import date
import requests          ##para descargar una imagen 
from PIL import Image    ##para convertir 0 y 1 a imagen
import io  
from selenium.common.exceptions import NoSuchElementException, ElementNotVisibleException
 
 
 
n=1
 
opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("disable-infobars")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36")
 
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
       
link_eliminar = [
                'https://www.c21bebrave.com/collections/liquidacion'        
                ]
 
 
porfolios=[]
for link in link_eliminar:
    driver.get(link)
    # while True:
    time.sleep(2)
    productos = driver.find_elements_by_xpath('//div[@data-product-id]')
    ##// para que nos busque en todos los hijos de la raiz en raiz
    
    for producto in productos[:1]:
     
        familia_subfamilia = driver.current_url
     
 
        try:
            url = str(producto.find_element_by_xpath('.//img').get_attribute('data-srcset'))
            url = "https:" + url.split(" ")[0]
            print(url)
            
            # con requests, hago el requerimiento a la URL de la imagen
            image_content = requests.get(url).content
         
            # PROCESAMIENTO DE LA IMAGEN
            image_file = io.BytesIO(image_content)
            image = Image.open(image_file).convert('RGB')
            file_path = './imagenes/'+'DUMMY.jpg' # nombre a guardar de la imagen
            with open(file_path, 'wb') as f:
                image.save(f, "JPEG", quality=85)
        except Exception as e:
            print(e)
            print ("Error")
        
 