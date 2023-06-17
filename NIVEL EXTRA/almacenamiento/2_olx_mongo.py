"""
OBJETIVO:  
    - Almacenar datos de OLX en MongoDB
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 9 ENERO 2023
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pymongo import MongoClient # pip install pymongo

client = MongoClient('localhost')
db = client['olx']
col = db['anuncios_selenium']

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()))

# Voy a la pagina que requiero
driver.get('https://www.olx.com.ar')

sleep(3)

for i in range(3): # Voy a darle click en cargar mas 3 veces
    try:
        # Esperamos a que el boton se encuentre disponible
        boton = WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )
        # le doy click
        boton.click()

        # espero hasta 10 segundos a que la informacion
        # en el ultimo elemento este cargada
        WebDriverWait(driver, 10).until(
          EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
        # Luego de que se halla el elemento, seguimos la ejecucion
    except Exception as e:
        print (e)
        # si hay algun error, rompo el lazo. No me complico.
        break

driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
sleep(5)
driver.execute_script("window.scrollTo({top: 20000, behavior: 'smooth'});")
sleep(5)
# Encuentro cual es el XPATH de cada elemento donde esta la informacion que quiero extraer
# Esto es una LISTA. Por eso el metodo esta en plural
autos = driver.find_elements('xpath', '//li[@data-aut-id="itemBox"]')

# Recorro cada uno de los anuncios que he encontrado
for auto in autos:
    # Por cada anuncio hallo el precio, que en esta pagina principal, a veces suele no estar
    try:
      precio = auto.find_element('xpath', './/span[@data-aut-id="itemPrice"]').text
    except:
      precio = 'NO DISPONIBLE'
    # Por cada anuncio hallo la descripcion
    descripcion = auto.find_element('xpath', './/span[@data-aut-id="itemTitle"]').text

    col.insert_one({
        'precio': precio,
        'descripcion': descripcion
    })
