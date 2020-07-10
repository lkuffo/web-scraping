"""
OBJETIVO:  
    - Aprender a realizar actualizacion de datos periodicamente a MongoDB desde Selenium
    - Aprender sobre los queries UPSERT
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 1 MAYO 2020
"""
import schedule
import time
from selenium import webdriver

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
    driver = webdriver.Chrome('./chromedriver.exe')

    for url in start_urls:
        driver.get(url)

        ciudad = driver.find_element_by_xpath('//h1').text
        current = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]').text
        real_feel = driver.find_element_by_xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]').text

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

while True:
    schedule.run_pending()
    time.sleep(1)
