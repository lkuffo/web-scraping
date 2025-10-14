from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor

class Farmacia(Item):
    nombre = Field()

    precio = Field()


class Ahumada(CrawlSpider):
    name = 'Farmacias'

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 50,
        'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36'
    }

    rules = (
        Rule(LinkExtractor(allow=r'/?cpage=\d+'), follow=True, callback="parse_farmacia")
    )

    download_delay = 1

    allowed_domains = ["farmaciasahumada.cl"]

    start_urls = ["https://www.farmaciasahumada.cl/catalogo-productos/"]

    def parse_farmacia(self, response):
        sel = Selector(response)

        productos = sel.xpath('//div[@class="col-md-9"]//div[@class="col-sm-12 col-md-3 "]')

        for producto in productos:
            item = ItemLoader(Farmacia(), producto)

            item.add_xpath('nombre', './/p[@class="n-gnc-bajada-pro-new"]//span[@class="t-com"]/text()')

            item.add_xpath('precio',
                           './/p[@class="n-gnc-bajada-pro-new"]//span[@class="n-gnc-bajada-precio-new"]/text()')

            yield item.load_item()

# CORRIENDO SCRAPY SIN LA TERMINAL
process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'data2.json'
})
process.crawl(Ahumada)
process.start()