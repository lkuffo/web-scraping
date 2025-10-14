from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
 
 
class Producto(Item):
    titulo = Field()
 
class Amazon(Spider):
    name = "Productos"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }
 
    start_urls = ['https://www.amazon.es/dp/B081S5NNNT']#URL de la que se va a extraer
 
    def parse(self, response):
        sel = Selector(response)
        item = ItemLoader(Producto(), sel)
 
        item.add_xpath('titulo', '//h1/span/text()')
        
        yield item.load_item()