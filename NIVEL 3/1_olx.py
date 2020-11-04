"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ABRIL 2020
"""
import random
from time import sleep
from selenium import webdriver # pip install selenium

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER

# Voy a la pagina que requiero
driver.get('https://www.olx.com.ec/autos_c378')
driver.refresh() # Solucion de un bug extraño en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento

sleep(5) # Esperamos que cargue el boton
# Busco el boton para cargar mas informacion

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
autos = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')


# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    # Por cada anuncio hallo el precio
    precio = auto.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print (precio)
    # Por cada anuncio hallo la descripcion
    descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print (descripcion)