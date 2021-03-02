from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Farmacia(Item):
    nombre = Field()
    precio = Field()
 
 
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
            item.add_xpath('nombre','.//div[@class="pdp-link"]/a/text()')
            #item.add_xpath('precio','.//div[contains(@class, "large-price")]//span[@class="value"]/text()')
 
            yield item.load_item()