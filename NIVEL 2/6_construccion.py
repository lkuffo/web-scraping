"""
OBJETIVO: 
    - Utilizar mas de una url semilla
    - Aprender a utilizar Web Scraping en la Nube con CRAWLERA
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 10 JULIO 2020
"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
 
class Departamento(Item):
    nombre = Field()
    direccion = Field()
 
 
class Urbaniape(CrawlSpider):
    name = "Departamentos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 5,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},
        'CRAWLERA_ENABLED': True,
        'CRAWLERA_APIKEY': 'INGRESA_TU_API_KEY'
    }

    """
    Este arreglo lo podriamos armar dinamicamente, algo tipo:
    start_urls = []
    for i in range (1, 100):
      start_urls.append('https://urbania.pe/buscar/proyectos-propiedades?page=' + str(i))
    """
    start_urls = [
      'https://urbania.pe/buscar/proyectos-propiedades?page=1',
      'https://urbania.pe/buscar/proyectos-propiedades?page=2'
    ] 

    allowed_domains = ['urbania.pe']
 
    download_delay = 1
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/proyecto-',
            ), follow=True, callback='parse_depa'),
    )
    def parse_depa(self, response):
        sel = Selector(response)
        item = ItemLoader(Departamento(),sel)
 
        item.add_xpath('nombre','//h2[@class="info-title"]/text()')
        item.add_xpath('direccion','//h2[@class="info-location"]/text()')
 
        yield item.load_item()