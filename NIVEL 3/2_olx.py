"""
OBJETIVO: 
    - Extraer el precio y el titulo de los anuncios en la pagina de OLX.
    - Aprender a utilizar la espera por eventos de Selenium.
    - Aprender a optimizar el tiempo de ejecucion de nuestras extracciones por Selenium de manera inteligente
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 14 SEPTIEMBRE 2023
"""
import random
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

opts = Options()
opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=opts)

# Voy a la pagina que requiero
driver.get('https://www.olx.in/')

# Cerramos dialogo de disclaimer (2024)
try:
    sleep(1)
    disclaimer_boton = driver.find_element(By.XPATH, '//button[@class="fc-button fc-cta-consent fc-primary-button"]')
    disclaimer_boton.click()
except:
    pass


for i in range(2): # Voy a darle click en cargar mas 2 veces
    try:
        # Esperamos a que el boton se encuentre disponible a traves de una espera por eventos
        # Espero un maximo de 10 segundos, hasta que se encuentre el boton dentro del DOM
        boton = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # le doy click al boton que espere
        boton.click()
        nAnuncios = 20 + (( i + 1 ) * 20 ) # 20 anuncios de carga inicial, y luego 20 anuncios por cada click que he dado
        # Espero hasta 10 segundos a que toda la informacion del ultimo anuncio este cargada
        WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//li[@data-aut-id="itemBox"][' + str(nAnuncios) + ']'))
        )
        # Luego de que se hallan todos los elementos cargados, seguimos la ejecucion
    except Exception as e:
        print (e)
        # si hay algun error, rompo el lazo. No me complico.
        break

# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
autos = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    # Por cada anuncio hallo el precio, que en esta pagina principal, rara vez suele no estar, por eso hacemos esta validacion.
    try:
      precio = auto.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    except:
      precio = 'NO DISPONIBLE'
    print (precio)
    # Por cada anuncio hallo la descripcion
    try:
      descripcion = auto.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text
    except:
      descripcion = 'NO DISPONIBLE'
    print (descripcion)


# Existen mas eventos que yo puedo esperar (VER RECURSOS)