 
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
from selenium.webdriver.common.action_chains import ActionChains
 
 
opts = Options()
opts.add_argument("start-maximized")
opts.add_argument("disable-infobars")
opts.add_argument("--disable-extensions")
opts.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
driver.get('https://drive.google.com/drive/folders/1mL-swjS-QPgw8DQzWJIjwUGw2wuP58cR')
time.sleep(5)

num_carpetas = driver.find_elements_by_xpath('//div[@role="main" and not(@style)]//div[@role="gridcell" and contains(@aria-label,"CDC")]')
imagenes = []
for i in range(0, len(num_carpetas)):
    carpetas = driver.find_elements_by_xpath('//div[@role="main" and not(@style)]//div[@role="gridcell" and contains(@aria-label,"CDC")]')
    carpeta = carpetas[i]

    carpeta.click()
    time.sleep(5)
   
    catalogo=driver.find_element_by_xpath('(//div[@data-target="folder"])[last()]').text
    referencias =driver.find_elements_by_xpath('(//div[@jsname="LpMIEc"])[last()]//c-wiz[@jsrenderer="zQdOjc"]')
    
    for r in referencias:
        
            try:
                soporte = catalogo
                print(soporte)
            except:
                soporte=""
                print(soporte)

            try:    
                referencia = r.find_element_by_xpath('.//div[@class="Q5txwe"]').text
                print(referencia)
            except:
                referencia=""
                print(referencia)

            imagenes.append({
                "catalogo":soporte,
                "referencia": referencia
                })
    driver.back()
    time.sleep(2)
driver.close()
 
df = pd.DataFrame(imagenes)