"""
OBJETIVO:  
    - Aprender a realizar actualizacion de datos periodicamente a MongoDB desde Scrapy
    - Aprender sobre los queries UPSERT
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 2 MAYO 2020
"""
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.spiders import Spider
from pymongo import MongoClient


client = MongoClient('localhost')
db = client['weather']
col = db['clima_scrapy']


class ExtractorClima(Spider):
    name = "MiCrawlerDeClima"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
        'CLOSESPIDER_PAGECOUNT': 20,
        'LOG_ENABLED': False
    }
    start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]
    def parse(self, response):
        print(response)
        ciudad = response.xpath('//h1/text()').get()
        current = response.xpath('//a[contains(@class, "card current")]//div[@class="temp"]/span[1]/text()').get()
        real_feel = response.xpath('//a[contains(@class, "card current")]//div[@class="real-feel"]/text()').get()
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

# Logica de automatizacion
runner = CrawlerRunner()
task = LoopingCall(lambda: runner.crawl(ExtractorClima))
task.start(20) # ejecutar cada 20 segundos
reactor.run()