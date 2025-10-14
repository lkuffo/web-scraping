from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import pandas as pd
from datetime import date
from datetime import datetime
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
 
Ftoday = date.today().strftime('%d%m%Y')
Fecha = date.today().strftime('%d-%m-%Y')
 
# Definimos el User Agent en Selenium utilizando la clase Options
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
#opts.add_argument('-headless')
driver = webdriver.Chrome('./chromedriver', chrome_options=opts) # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
 
#URL SEMILLA
 
start_urls = ["https://www.numbeo.com/property-investment/region_rankings.jsp?title=2021&region=019"]
 
i=0
for url in start_urls:
    driver.get(url)
 
    Titulo=driver.find_element(By.XPATH,'//div[2]/h1').text 
    
    f = open("./"+Titulo+".csv", "a")
    f.close()
      
    
    seleccionador = driver.find_element(By.XPATH, '//form[1]/select')
    opciones=seleccionador.find_elements_by_tag_name("option")
    textos = []
    for opcion in opciones:
      textos.append(opcion.text)

    for texto in textos:  
        try:
            print(texto)
            # Esperamos a que el boton se encuentre disponible a traves de una espera por eventos
            # Espero un maximo de 10 segundos, hasta que se encuentre el boton dentro del DOM
            seleccionador = driver.find_element(By.XPATH, '//select[@name="title"]').click()
            boton = WebDriverWait(driver, 10).until(
              EC.presence_of_element_located((By.XPATH, "//form[1]/select/option[.='"+ texto + "']"))
            )
            # le doy click al boton que espere
            boton.click()

            nombre_encabezados = []
            encabezados = driver.find_elements_by_xpath('//table[@id="t2"]//thead//th/div/div')
            for encabezado in encabezados:
              nombre_encabezados.append(encabezado.text)
            
            valores = []
            filas_tabla = driver.find_elements_by_xpath('//table[@id="t2"]//tbody/tr')
            for fila in filas_tabla:
              valores_fila = fila.find_elements_by_xpath('.//td')
              fila = []
              for valor in valores_fila:
                fila.append(valor.text)
              valores.append(fila)
            
            print(nombre_encabezados) # nombre de encabezados
            print(valores) # lista de listas, cada lista es una fila y sus valores
 
        except Exception as e:
            print (e)
            # si hay algun error, rompo el lazo. No me complico.
            break
