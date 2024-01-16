"""
OBJETIVO:  
    - Inicio de sesion a partir de formulario con scrapy
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 16 ENERO 2024
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess
import scrapy


class LoginSpider(Spider):
    name = 'GitHubLogin'
    start_urls = ['https://github.com/login']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'lkuffo', 'password': open('./password.txt').readline().strip()},
            callback=self.after_login
        )

    def after_login(self, response):
        request = scrapy.Request(
            'https://github.com/lkuffo?tab=repositories',
            callback=self.parse_repositorios
        )
        yield request

    def parse_repositorios(self, response):
        sel = Selector(response);
        repositorios = sel.xpath('//h3[@class="wb-break-all"]/a/text()')
        for repositorio in repositorios:
            print(repositorio.get())


process = CrawlerProcess({
    'FEED_FORMAT': 'json',
    'FEED_URI': 'datos_de_salida.json'
})
process.crawl(LoginSpider)
process.start()
