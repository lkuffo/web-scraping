"""
OBJETIVO:  
    - Aprender a automatizar la ejecucion de extracciones en Selenium y requests.
    - Aprender a utilizar la libreria Schedule para agendar/automatizar procesos por intervalos.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 9 ENERO 2023
"""
import schedule # pip install schedule
import time
from selenium import webdriver

start_urls = [
    "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
    "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
    "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]

def extraer_datos():
    driver = webdriver.Chrome('./chromedriver')

    # Por cada una de las URLs que quiero extraer...
    for url in start_urls:

        # Voy en mi navegador a cada URL
        driver.get(url)

        # Extraigo los datos
        ciudad = driver.find_element('xpath', '//h1').text
        current = driver.find_element('xpath', '//div[contains(@class, "cur-con-weather-card__body")]//div[@class="temp"]').text
        real_feel = driver.find_element('xpath', '//div[contains(@class, "cur-con-weather-card__body")]//div[@class="real-feel"]').text

        # Limpieza de datos
        ciudad = ciudad.replace('\n', '').replace('\r', '').strip()
        current = current.replace('C', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        real_feel = real_feel.replace('RealFeel®', '').replace('°', '').replace('\n', '').replace('\r', '').strip()
        
        # Guardado de datos en un archivo
        f = open("./datos_clima_selenium.csv", "a")
        f.write(ciudad + "," + current + "," + real_feel + "\n")
        f.close()
        print(ciudad)
        print(current)
        print(real_feel)
        print()

    # Cierro el navegador
    driver.close()


# Logica de schedule (ver documentacion en recursos)
schedule.every(1).minutes.do(extraer_datos) # Cada 1 minuto ejecutar la funcion extraer_datos

# Reviso la cola de procesos cada segundo, para verificar si tengo que correr algun proceso pendiente
while True:
    schedule.run_pending() # Correr procesos que esten pendientes de ser ejecutados.
    time.sleep(1) # Para no saturar el CPU de mi maquina (por el while true), espero 1 segundo entre cada iteracion
