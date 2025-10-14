import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
 
class Artículo(Item):
    título = Field()
    precio = Field()
    descripción = Field()
 
class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    download_delay = 1
 
    allowed_domains = ['articulo.mercadolibre.com.ec', 'listado.mercadolibre.com.ec']   #puedo poner más dominios solo poniendo comas
 
    start_urls = ['https://listado.mercadolibre.com.ec/perros#D[A:perros,L:undefined]']
 
    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+'
            ), follow=True),
 
        Rule(   # REGLA #2 => VERTICALIDAD AL DETALLE PRODUCTOS
            LinkExtractor(
                allow=r'/MEC-'
            ), follow=True, callback='parse_items'),
    )
 
    def parse_items(self, response):
        item = ItemLoader(Artículo(), response)
 
        item.add_xpath('título', '//h1/text()')
        item.add_xpath('descripción', '//div[@class="item-description__text"]/p/text()')
        item.add_xpath('precio', '//span[@class="price-tag-fraction"]/text()')
 
        yield item.load_item()