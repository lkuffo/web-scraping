import scrapy
from twisted.internet import reactor
from scrapy.loader import ItemLoader
from scrapy import Selector, item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.item import Field
from scrapy.loader.processors import MapCompose
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor

class ProductItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()
 
 
class CaWalmartSpider(CrawlSpider):
    name = "ca_walmart"
    allowed_domains = ["walmart.ca"]
    start_urls = ["https://www.walmart.ca/en/grocery/fruits-vegetables/fruits/N-3852"]
    custom_settings = { # TIENE UN USER AGENT MUY MUY ESPECIAL. SIN ESTE USER AGENT NO FUNCIONA
        'USER_AGENT': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; http://www.google.com/bot.html) Chrome/W.X.Y.Z‡ Safari/537.36 '
    }
 
    download_delay = 3
 

    rules = (
        Rule(  # Regla de movimiento VERTICAL hacia el detalle de los itemns
            LinkExtractor(
                allow=r'/ip/',  # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_item"),
    # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )
 
    def parse_item(self, response):
        print(response)
        sel = Selector(response)
        item = ItemLoader(ProductItem(), sel)
        item.add_xpath('name', '//div[@class="css-j7qwjs e1yn5b3f0"]/h1/text()')
        item.add_xpath('price', '//div[@class="css-k008qs e1ufqjyx0"]/span/text()')
        yield item.load_item()