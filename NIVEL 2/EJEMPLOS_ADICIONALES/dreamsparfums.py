from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Producto(Item):
    stock = Field()
    precio = Field()
    descripcion = Field()

class dreamsparfums(CrawlSpider):
    name = "ProductosDreams"
 
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100,
        'CLOSESPIDER_ITEMCOUNT': 2
    }
 
    #allowed_domains = ['dreamsparfums.cl']
    start_urls = ['https://www.dreamsparfums.cl/3-perfumes']
 
    download_delay = 1
 
    rules = (
        #paginacion(h)
        Rule(
            LinkExtractor(
                allow='page=\d+'
            ), follow=True
        ),
        #detalles productos(v)
        Rule(
            LinkExtractor(
                allow=r'/catalogo/'
            ), follow=True, callback="parse_producto"
        ),
    )
 
    def parse_producto(self, response):
        #sel = Selector(response)
        item = ItemLoader(Producto(), response)
        #item.add_xpath('nombre', '')
        item.add_xpath('stock', '//div[@class="product-information"]//span[@data-allow-oosp="0"]/text()')
        item.add_xpath('precio', '//div[@class="current-price"]/span/text()')
        item.add_xpath('descripcion', '//div[@class="product-information"]/div[@itemprop="description"]/text()')
 
        yield item.load_item()