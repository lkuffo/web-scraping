from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
 
class Articulo(Item):
     nombre = Field()
 
class mercantilSpider(CrawlSpider):
    name = 'mercantil'
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 20 
    }
    allowed_domains = ['mercantil.com']
    start_urls = ['https://www.mercantil.com/clinicas/metropolitana/499']
    download_delay = 1
    rules = (
        Rule(   
            LinkExtractor(
                allow=r'/empresa/' 
            ), follow=True, callback='parse_items'),
    )
    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)                
        item.add_xpath('nombre', '//div[@class="empresas_title"]/h1/a/text()')        
        yield item.load_item()