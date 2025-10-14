from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from time import sleep
import random
 
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', chrome_options=opts)
driver.get("https://www.eleconomista.com.mx/tags/paquete-economico-2021-18122")
 
for i in range(3):    
    try:
        boton=WebDriverWait(driver,6).until(
            EC.presence_of_element_located((By.XPATH,'//div[@class="entrys-con-banner last clearfix"]//a[@class="btn"]'))
        )
        boton.click()
    except Exception as e:
        print(e)
        break
        
ElEconomista=[]
 
articulos=driver.find_elements_by_xpath('//article[@itemtype="http://schema.org/Article"]')
 
for articulo in articulos:
    try:
      autor=articulo.find_element_by_xpath('.//p/a').text
    except:
      autor="NA"
    try:
      titulo=articulo.find_element_by_xpath('.//div[@class="entry-data"]/h3/a').text
    except:
      autor="NA"
    try:
        nota=articulo.find_element_by_xpath('.//div[@class="entry-data"]/p').text 
    except:
        nota="NA"
    
    #se crea un diccionario para cada item
    articulo_dict=dict()
    articulo_dict["autor"]=autor
    articulo_dict["titulo"]=titulo
    articulo_dict["nota"]=nota
    
    ElEconomista.append(articulo_dict)

print (ElEconomista)
 