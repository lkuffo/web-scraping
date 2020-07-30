import random
from time import  sleep
from  selenium import  webdriver
 
 
driver = webdriver.Chrome('./chromedriver')
 
driver.get('https://douglas.es/c/perfumes')
 
 
# todos los productos en una lista
productos =driver.find_elements_by_xpath('//div[@class="rd__product-tile sd__product-tile"]')
                                        ##// para que nos busque dentro de la ruta esprecificada
for producto in productos:
    descripcion = producto.find_element_by_xpath('.//a[@class="rd__copytext rd__copytext--90 rd__bb-productinfo__name rd__item-basketflyout__copytext"]').text
    print(descripcion)
    precio_activo = producto.find_element_by_xpath('.//span[contains(@class,"rd__productinfo__price--sale")]').text
    print(precio_activo)
 