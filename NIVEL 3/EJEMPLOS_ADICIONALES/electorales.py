import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from time import sleep
 
opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36")
driver = webdriver.Chrome('./chromedriver', options=opts)
 
driver.get('https://plataformaelectoral.jne.gob.pe/ListaDeCandidatos/Index')
driver.refresh()
sleep(5)
boton = driver.find_element_by_xpath('//button[@class="button button--is-primary bg--is-red"]')
sleep(5)
boton.click()
sleep(random.uniform(3.0, 4.0))
 
#boton2 = driver.find_element_by_xpath('//a[@class="pages__number Pages100"]')
#sleep(3)
#boton2.click()
 
boton2 = driver.find_element_by_xpath('//div[@class="VotonesVerMas"]')
sleep(3)
boton2.click()
sleep(random.uniform(3.0, 4.0))
tablas = driver.find_elements_by_xpath('.//table[@class="tablas-estilos alineado-izquierda tabla-limites tabla-notificacion"]')
 
for tabla in tablas:
 id = tabla.find_element_by_xpath('.//thead/tr[@class="cabecera-bandeja"]/th[8]').text
 id2 = tabla.find_element_by_xpath('.//thead/tr[@class="cabecera-bandeja"]/th[9]').text
 id3 = tabla.find_element_by_xpath('.//thead/tr[@class="cabecera-bandeja"]/th[10]').text
 id4 = tabla.find_element_by_xpath('.//thead/tr[@class="cabecera-bandeja"]/th[11]').text
 id5 = tabla.find_element_by_xpath('.//thead/tr[@class="cabecera-bandeja"]/th[12]').text
 
 print (id+","+id2+","+id3+","+id4+","+id5)