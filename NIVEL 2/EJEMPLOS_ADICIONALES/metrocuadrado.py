from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class Inmueble(Item):
  Descripcion = Field()
  Precio = Field()
  Area = Field()

class MetrocuadradoCrawler(CrawlSpider):
    name="MetroCuadrado"
    custom_settings={
        'USER_AGENT':'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    
    download_delay=2
    allowed_domains=['metrocuadrado.com']
    start_urls=['https://www.metrocuadrado.com/oficinas/arriendo/medellin/']
    rules=(
        # Detalle de los inmuebles
        Rule(LinkExtractor(
            allow=r'/inmueble/'), follow=True, callback='parse_items'
        ),
        # Paginacion
        Rule(LinkExtractor(
            allow=r'/#'), follow=True
        ),
    )
    
    def parse_items(self, response):
        
        item = ItemLoader(Inmueble(),response)
        item.add_xpath('Descripcion','//h1[@itemprop="headline"]/text()')
        item.add_xpath('Precio','//dd[@class="important"]/text()')
        item.add_xpath('Area','//dd/h4/text()')
        
        yield item.load_item()
    
if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
    process = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'output.json'
    })
    process.crawl(MetrocuadradoCrawler)
    process.start()