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
# opts.add_argument("download.default_directory=C:/Downloads")
# instalando del driver de selenium que va a controlar nuestro navegador
# a partir de este objeto voy a crear web scraping e interacciones
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
 
 
# voy a la pagina que requiero
#######################################################################################################################
#######################################################################################################################
driver.get('https://douglas.es/')
 
#cogo el link de cada familia
#################################
 
links_familias=driver.find_elements_by_xpath('.//a[@class="rd__link rd__copytext--30"]')
links_por_familia =[]
# link_por_subfamilia=[]
for tag_a in links_familias:
        links_por_familia.append(tag_a.get_attribute("href"))
#################################
 
#cogo el link de las subfamilias
###############################
links_por_subfamilia=[]
for familia in links_por_familia:
    driver.get(familia)  
    time.sleep(2)                
    links_subfamilias=driver.find_elements_by_xpath('.//a[@class="rd__copytext rd__copytext--100"]')  
    # links_por_subfamilia=[]
    for tag_b in links_subfamilias:
        links_por_subfamilia.append(tag_b.get_attribute("href"))

print("Links a visitar: ", len(links_por_subfamilia))
####creo la lista vacia que voy a rellenar de variables 
porfolios = []         
for link in links_por_subfamilia:
   driver.get(link)
   sleep(1)
   familia_subfamilia = driver.find_element_by_xpath('.//h1').text
   max_pag = 0
   while True:
   # todos los productos en una lista
       productos = driver.find_elements_by_xpath('//div[@class="rd__product-tile sd__product-tile"]')
       ##// para que nos busque en todos los hijos de la raiz en raiz
 
       for producto in productos:
      
        
           marca = producto.find_element_by_xpath('.//a[@class="rd__headline rd__headline--80 sd__bold rd__eye-catcher__text"]').text
        
           descripcion = producto.find_element_by_xpath('.//a[@class="rd__copytext rd__copytext--90 rd__bb-productinfo__name rd__item-basketflyout__copytext"]').text
           print(descripcion)  ## . para que nos busque en los hijos de del elemento productos // para que haga la busqueda
 
           precio_activo = producto.find_element_by_xpath('.//span[contains(@class,"rd__productinfo__price--sale")]').text
           print(precio_activo)
        
           pvp = producto.find_element_by_xpath('.//s[contains(@class,"rd__productinfo__sale-price")]').text
 
           porfolios.append({
                "familia_subfamilia":familia_subfamilia,                        
                "marca":marca,
                "descripcion":  descripcion,
                "precio_venta": precio_activo,
                "pvp_regular":pvp
            })
       max_pag += 1
 
       if (max_pag == 3): break
       time.sleep(5)
       try:
           scrollingScript = """ 
            document.getElementsByClassName('section-layout section-scrollbox scrollable-y scrollable-show')[0].scroll(0, 2000000)
           """
           driver.execute_script(scrollingScript)
           driver.find_element_by_xpath('//a[contains(@class,"rd__pagination__next")]').click()
           print("Navigating to Next Page")
       except (TimeoutException, WebDriverException) as e:
           print(e)
           print("Last page reached")
           break
         
 
driver.close()
 
df = pd.DataFrame(porfolios)
print(df)
df["pvps"]= df["pvp_regular"].str.split("/").str.get(0)
df["p_venta"] = df["precio_venta"].str.split("/").str.get(0)
df["cant"] = df["precio_venta"].str.split("/").str.get(1)
del df["precio_venta"]
del df["pvp_regular"]
print(df)
# df.to_csv("douglas.csv",sep="|")   