import random
from time import  sleep
from  selenium import  webdriver
 
 
driver = webdriver.Chrome('./chromedriver')
 
driver.get('http://www.mitramiss.gob.es/estadisticas/eat/welcome.htm')
 
 
boton_descarga = driver.find_element_by_xpath("//input[@onclick='ir_a(document.f_lista.listaIE); return false;']")
 
boton_descarga.click()