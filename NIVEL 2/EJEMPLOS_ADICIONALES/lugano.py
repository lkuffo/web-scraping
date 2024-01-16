"""
OBJETIVO: 
    - Solidificar los conocimientos de Scrapy
    - Utilizar más lógica de programación para almacenar información (contrario a directamente siempre almacenar lo que haya dentro de un XPATH)
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 NOVIEMBRE 2023
"""

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Morral(Item):
    nombre = Field()
    descripcion = Field() 
    precio = Field()
    
class TripAdvisor(CrawlSpider):
    name = "Morrales"
    custom_settings = {
        'USER_AGENT': "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }   
    start_urls = ['https://www.lugano.com.co/morrales']
    allowed_domains = ['lugano.com.co']
    download_delay = 2

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/morral-'
            ), follow=True , callback="parse_morral"
        ),
    )
    
    def limpiar_precio(self, texto):
        nuevoTexto=texto.replace("$","").strip()
        return nuevoTexto
    
    def parse_morral(self, response):
        sel = Selector(response)
        item = ItemLoader(Morral(), sel)
       
       
        item.add_xpath('nombre','//h1[@class="product-name"]/a/text()')
        item.add_xpath('descripcion','//div[@id="collapseOne"]/div[@class="panel-body tipgor"]/p/text()')

        precio_sin_descuento = sel.xpath('//del[@class="amount"]//span[@class="money"]/text()').get()
        precio_con_descuento = sel.xpath('//label[@class="amount"]//span[@class="money"]/text()').get()
        print(precio_con_descuento)
        if self.limpiar_precio(precio_con_descuento) == '0':
            precio = precio_sin_descuento
        else:
            precio = precio_con_descuento
        item.add_value('precio', self.limpiar_precio(precio))   
        
        yield item.load_item()