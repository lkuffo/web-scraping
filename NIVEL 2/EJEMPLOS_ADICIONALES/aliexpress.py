from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Articulo(Item):
    titulo = Field()
    precio = Field()
 
class aliexpresscrawl(Spider):
    name = "aliexpress"
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    download_delay = 2
    start_urls = ['https://es.aliexpress.com/af/impresoras-3d.html?d=y&origin=n&SearchText=impresoras+3d&catId=0&initiative_id=SB_20200608070330']
 
    allowed_domains = ['es.aliexpress.com']

    def parse(self, response):
      print(response.text)
