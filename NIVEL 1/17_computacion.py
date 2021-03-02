from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class Computrabajo(Item):

    puesto = Field()



# Clase core

class SpiderCompu(Spider):

    name = "SpiderCompu"

    custom_settings = {"USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"

                      }

    start_urls = ['https://www.computrabajo.com.ar/empleos-de-informatica-y-telecom']

 

    def parse(self, response):

        sel = Selector(response)

        puestos = sel.xpath("//div[@class='iO']")

        for puesto in puestos:

            item = ItemLoader(Computrabajo(), puestos)

            item.add_xpath("puesto", ".//h2/a/text()")

           

            yield item.load_item()



process = CrawlerProcess({

    'FEED_FORMAT': 'csv',

    'FEED_URI': 'resultados1.csv'

     })

process.crawl(SpiderCompu)

process.start()