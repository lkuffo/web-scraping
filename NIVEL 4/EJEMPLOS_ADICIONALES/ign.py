"""
===========================================
============= DESACTUALIZADO ==============
==== IGN AHORA UTILIZA OTRA PAGINA ========
===========================================
OBJETIVO: 
    - Extraer el titulo, fecha de publicacion y duracion de un video de IGN.
    - Aprender a extraer datos de iframes desde Scrapy
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 3 ABRIL 2020
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy import Request

class Video(Item):
  titulo = Field()
  fecha_de_publicacion = Field()
  duracion = Field()


class IGNCrawler(CrawlSpider):
  name = 'ign'
  custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
    'CLOSESPIDER_PAGECOUNT': 100,
    'REDIRECT_ENABLED': True
  }

  allowed_domains = ['latam.ign.com', 'widgets.ign.com', 'g.ign.com']
  start_urls = ['https://latam.ign.com/dragon-ball-z-kakarot/69217/video/trailer-del-dlc-de-dragon-ball-z-kakarot']

  download_delay = 1

  def parse(self, response):
    sel = Selector(response)
    titulo = sel.xpath('//h1/text()').get()
    fecha_de_publicacion = sel.xpath('//span[@class="publish-date"]/text()').get()

    previous_data = {
      'titulo': titulo,
      'fecha_de_publicacion': fecha_de_publicacion
    }

    iframe_url = sel.xpath('//iframe[@class="vplayer"]/@src').get()

    print (iframe_url)

    yield Request(iframe_url, callback = self.parse_iframe, meta=previous_data)

  def parse_iframe(self, response):
    print ("HOLAA", response.text)
    item = ItemLoader(Video(), response)
    item.add_xpath('duracion', '//div[@class="duration"]/text()')
    item.add_value('titulo', response.meta.get('titulo'))
    item.add_value('fecha_de_publicacion', response.meta.get('fecha_de_publicacion'))

    yield item.load_item()


# EJECUCION
# scrapy runspider ign.py -o ign.json -t json