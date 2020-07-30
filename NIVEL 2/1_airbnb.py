"""
===========================================
============= DESACTUALIZADO ==============
=== AIRBNB AHORA UTILIZA CARGA DINAMICA ===
===========================================
OBJETIVO: 
    - Extraer informacion sobre los establecimientos de AIRBNB.
    - Aprender a realizar extracciones verticales utilizando reglas
    - Aprender a utilizar MapCompose para realizar limpieza de datos
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 1 ABRIL 2020
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Habitacion(Item):
  titulo = Field()
  huespedes = Field()
  caracteristicas = Field()
  


class AirbnbCrawlerVertical(CrawlSpider):
  name = "CrawlerVertical"
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
  }
  start_urls = ["https://www.airbnb.com.ar/s/Buenos-Aires--Ciudad-Aut%C3%B3noma-de-Buenos-Aires--Argentina/homes"]
  
  allowed_domains = ["airbnb.com.ar"]
  download_delay = 1
  rules = (
    Rule(LinkExtractor(allow=r'/rooms'), callback = 'parse_items'),
  )

  def procesarHuespedes(self, texto):
    if (texto and len(texto) > 1):
      texto_dividido = texto.split(' ')
      return texto_dividido[0]
    return '0'
    

  def parse_items(self, response):
    sel = Selector(response)
    item = ItemLoader(Habitacion(), sel)
    item.add_xpath('titulo', '//h1/text()')

    item.add_xpath('huespedes', '//*[@id="site-content"]/div/div[4]/div/div/div[1]/div[1]/div/div/div/div/section/div/div/div/div[1]/div[2]/span[1]/text()', MapCompose(self.procesarHuespedes))

    item.add_xpath('caracteristicas', '//div[@data-plugin-in-point-id="AMENITIES_DEFAULT"]//div[@class="_1nlbjeu"]/div[1]/text()')
    yield item.load_item()