"""	
===========================================
============= CLASE OBSOLETA ==============
====== AHORA UTILIZA CARGA DINAMICA =======
====== QUEDA COMO CLASE DEMOSTRATIVA ======
===========================================
OBJETIVO: 	
    - Aprender a utilizar Link Extractor de una manera mas sofisticada	
CREADO POR: LEONARDO KUFFO	
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
 
class Farmacia(Item):
    Nombre = Field()
    Precio = Field()
 
 
class CruzVerdeSpider(CrawlSpider):
    name = 'CruzVerde'
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    allowed_domains = ['cruzverde.cl']
    start_urls = ["https://www.cruzverde.cl/medicamentos/"]
    download_delay = 1
 
    rules = (
        # Horizontal por tipo de informacion
        Rule(
            LinkExtractor(
                allow=r'start=',
                tags=('a', 'button'),
                attrs=('href', 'data-url')
            ), follow=True, callback='parse_farmacia'
        ),
    )
    def parse_farmacia(self, response):
        sel = Selector(response)
 
        productos = sel.xpath('//div[@class="col-12 col-lg-4"]')
 
        for producto in productos:
            item= ItemLoader(Farmacia(), producto)
            item.add_xpath('Nombre', './/div[@class="tile-body px-3 pt-3 pb-0 d-flex flex-column pb-0"]//div[@class="pdp-link"]/a/text()')
            item.add_xpath('Precio', './/span[contains(@class, "value ")]/text()')
 
            yield item.load_item()

# EJECUCION	
# scrapy runspider 2_mercadolibre.py -o mercado_libre.json -t json 