"""
OBJETIVO: 
    - Utilizar mas de una url semilla
    - Aprender a utilizar Web Scraping en la Nube con Zyte
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 08 ABRIL 2024
"""
from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

from itemloaders.processors import MapCompose
 
class Departamento(Item):
    nombre = Field()
    direccion = Field()
 
 
class Urbaniape(CrawlSpider):
    name = "Departamentos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'CLOSESPIDER_ITEMCOUNT': 5,
        'DOWNLOADER_MIDDLEWARES': {'scrapy_zyte_smartproxy.ZyteSmartProxyMiddleware': 610},
        'ZYTE_SMARTPROXY_ENABLED': True,
        'ZYTE_SMARTPROXY_URL': 'http://api.zyte.com:8011', # Migracion a Zyte API (Abril 2024)
        'ZYTE_SMARTPROXY_APIKEY': '<SU_API_KEY>'
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
                allow=r'/proyecto/',
            ), follow=True, callback='parse_depa'),
    )

    def limpiar_texto(self, texto):
        return texto.replace('\n', '').replace('\t', '').replace('\r', '')

    def parse_depa(self, response):
        sel = Selector(response)
        item = ItemLoader(Departamento(),sel)
 
        item.add_xpath('nombre','//h1/text()',
                       MapCompose(self.limpiar_texto))
        item.add_xpath('direccion','//section[@id="map-section"]/div[@class="section-location-property"]/h4/text()',
                       MapCompose(self.limpiar_texto))
 
        yield item.load_item()