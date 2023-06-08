from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup


class Analisis(Item):
    nombre = Field()
    precio = Field()


class ChopoCrawler(CrawlSpider):

    name = 'chopo'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 30
    }

    allowed_domains = ['chopo.com.mx']

    start_urls = ['https://www.chopo.com.mx/ensenada/estudios/laboratorio']

    download_delay = 1

    # Tupla de reglas

    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION, el problema es que la página se cambia con scroll
            LinkExtractor(
                allow=r'\?p=',
                tags=('a', 'link'),
                attrs=('href'),
            ), follow=True, callback='parse_items'),
    )


    def parse_items(self, response):
        sel = Selector(response)
        pruebas = sel.xpath('//li[@class="catalog-grid-item product-item-details product-item-info"]')

        for prueba in pruebas:
            item = ItemLoader(Analisis(), prueba)
            item.add_value('nombre', './/h2[@class="catalog-grid-item__name"]/a/text()')
            precio = response.xpath('.//span[@class="price"]/text()').extract_first()
            if precio is not None:
                item.add_xpath('precio', './/span[@class="price"]/text()')   
            else:
                item.add_xpath('precio', './/span[@class="price-tag-fraction"]/text()') 
            yield item.load_item()


# scrapy runspider 15_laboratorio.py -o ChopoScrapy01.csv -t csv