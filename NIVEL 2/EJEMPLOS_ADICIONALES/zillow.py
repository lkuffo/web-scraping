from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
 
 
class info(Item):
   price=Field()
   
 
class zillowCrawler (CrawlSpider):
   name='zillow'
   custom_settings={
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT':20
   }
 
   download_delay=1
 
   allowed_domains = ['zillow.com']
 
   start_urls=['https://www.zillow.com/homes/Charlotte,-NC_rb/']
 
   rules = (
      Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
         LinkExtractor(
            allow=r'/homes'
            # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
         ), follow=True),
      Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
         LinkExtractor(
            allow=r'/homedetails'
         ), follow=True,
         callback='parse_items'),
 
   )
   def parse_items(self, response):
 
      item=ItemLoader(info(), response)
      item.add_xpath('price', '//span[@class="ds-value"]/text()')
      
 
      yield item.load_item()