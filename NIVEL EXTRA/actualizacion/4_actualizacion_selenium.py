"""
OBJETIVO:  
    - Aprender a realizar actualizacion de datos periodicamente a MongoDB desde Selenium
    - Aprender sobre los queries UPSERT
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""
import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from pymongo import MongoClient # pip install pymongo
client = MongoClient('localhost')
db = client['weather']
col = db['clima']

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]

def extraer_datos():
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36")
    # Agregar a todos sus scripts de selenium para que no aparezca la ventana de seleccionar navegador por defecto: (desde agosto 2024)
    opts.add_argument("--disable-search-engine-choice-screen")

    # Instancio el driver de selenium que va a controlar el navegador
    # A partir de este objeto voy a realizar el web scraping e interacciones
    driver = webdriver.Chrome(options=opts)

    for url in start_urls:
        driver.get(url)

        ciudad = driver.find_element('xpath', '//h1').text
        current = driver.find_element('xpath', '//div[contains(@class, "cur-con-weather-card__body")]//div[@class="temp"]').text
        real_feel = driver.find_element('xpath', '//div[contains(@class, "cur-con-weather-card__body")]//div[@class="real-feel"]').text

        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Debo elegir cual de mis propiedades va a ser UNICA a lo largo de todos los documentos
        col.update_one({
            'ciudad': ciudad # En este caso es mi ciudad, es decir. Por esta condicion voy a buscar para actualizar
        }, {
            '$set': { # Si no se encuentra ni un documento con el identificador, se inserta un documento nuevo
                'ciudad': ciudad, # Si si se encuentra un documento con el identificador, se actualiza ese documento con la nueva informacion
                'current': current,
                'real_feel': real_feel
            }
        }, upsert=True) # Flag para utilizar la logica de Upsert

        print(ciudad)
        print(current)
        print(real_feel)
        print()
    driver.close()


# Logica de automatizacion de extraccion
schedule.every(5).minutes.do(extraer_datos) # Cada 5 minutos ejecuta la extraccion
# Llamamos a la funcion fuera del lazo para una primera llamada instantanea
extraer_datos()
while True:
    schedule.run_pending()
    time.sleep(1)
