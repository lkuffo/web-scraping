"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX autos.
    - Aprender a realizar extracciones que requieran una accion de click para cargar datos.
    - Introducirnos a la logica de Selenium
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 27 MAYO 2023
"""

#####
### ATENCION: OLX necesita que le demos permisos de geolocalizacion al navegador de selenium para que nos muestre los datos
### Esto lo haremos una unica vez en la primer corrida del programa. Este problema es mas comun en usuarios de MAC
#####
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver # pip install selenium

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome('./chromedriver') # REMPLAZA AQUI EL NOMBRE DE TU CHROME DRIVER
# Voy a la pagina que requiero
driver.get('https://www.olx.com.ar/autos_c378')
sleep(3)
driver.refresh() # Solucion de un bug extraño en Windows en donde los anuncios solo cargan al hacerle refresh o al darle click a algun elemento
sleep(5) # Esperamos que cargue el boton
# Busco el boton para cargar mas informacion
boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
for i in range(3): # Voy a darle click en cargar mas 3 veces
    try:
        # le doy click
        boton.click()
        # espero que cargue la informacion dinamica
        sleep(random.uniform(8.0, 10.0))
        # busco el boton nuevamente para darle click en la siguiente iteracion
        boton = driver.find_element(By.XPATH, '//button[@data-aut-id="btnLoadMore"]')
    except:
        # si hay algun error, rompo el lazo. No me complico.
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
autos = driver.find_elements(By.XPATH, '//li[@data-aut-id="itemBox"]')


# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    try:
        # Por cada anuncio hallo el precio
        precio = auto.find_element(By.XPATH, './/span[@data-aut-id="itemPrice"]').text
        print (precio)
        # Por cada anuncio hallo la descripcion
        descripcion = auto.find_element(By.XPATH, './/div[@data-aut-id="itemTitle"]').text
        print (descripcion)
    except Exception as e:
        print ('Anuncio carece de precio o descripcion')
