from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()


class ElCorteInglesCrawler(CrawlSpider):

    name = 'ElCorteIngles'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'FEED_EXPORT_FIELDS': ['titulo', 'precio', 'descripcion'],
        'CLOSESPIDER_ITEMCOUNT': 50
    }

    start_urls = [
      'https://www.elcorteingles.es/supermercado/alimentacion-general/'
    ]

    allowed_domains = ['elcorteingles.es']

    rules = (
      Rule(
        LinkExtractor(
          allow=r'/\d+/'
        ), 
        follow=True), 
      Rule(
        LinkExtractor(
          allow=r'/\d+-'
        ), follow=True, callback='parse_items'),
    )

    def parse_start_url(self, response):
      print(response.body)
    
    def parse_items(self, response):

        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//div[@class="pdp-title mb"]/text()')
        item.add_xpath('descripcion', '//div[@class="pdp-info-container"]/text()')
        item.add_xpath('precio', '//div[@class="prices pdp-prices"]/text()')

        yield item.load_item()



process = CrawlerProcess({
  'FEED_FORMAT': 'csv', 
  'FEED_URI': 'elcorteingles.csv'
})

process.crawl(ElCorteInglesCrawler)

process.start()