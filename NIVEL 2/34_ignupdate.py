from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess
from scrapy.loader.processors import MapCompose #editar un dato de un arbol html
from scrapy.linkextractors import LinkExtractor
 
#Definir los diferentes tipos de extracción que deseo realizar
 
class Articulo(Item):
    titulo = Field()
    contenido = Field()
 
class Review(Item):
    titulo_r = Field()
    calificacion_r = Field()
 
class Video(Item):
    titulo_v = Field()
    fecha_v = Field()
 
class IGNCrawler(CrawlSpider):
    name = 'ign'
 
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
        , 'FEED_EXPORT_ENCODING': 'utf-8'
        , 'CLOSESPIDER_PAGECOUNT': 50
    }
 
    start_urls = ['https://latam.ign.com/se/?model=&q=Nintendo+Switch']
 
    '''Para protegerse de baneos, se debe tener un delay entre cada requerimiento, ya se van hacer varias paginas a las cuales se van hacer peticiones'''
    download_delay = 2  # Tiempo en segundos
    '''configuramos los dominios para limitar el espectro de busqueda'''
    allowed_domains = [
        'latam.ign.com'
    ]
 
 
 
    rules = (
        # Horizontal por tipo de información
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True
        ),
        # Horizontal por tipo de paginación
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ), follow=True
        ),
        # Una regla por cada tipo de contenido donde ire verticalmente
        #Reviews
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ), follow=True, callback='parse_ign_review'
        ),
        #Videos
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ), follow=True, callback='parse_ign_video'
        ),
        #Articulos
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ), follow=True, callback='parse_ign_new'
        ),
    )
 
    def parse_ign_review(self, response):
        sel1 = Selector(response)
        item = ItemLoader(Review(), sel1)
        item.add_xpath('titulo_r', '//div[@class="article-headline"]//h1/text()')
        item.add_xpath('calificacion_r', '//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')
 
        yield item.load_item()
 
    def parse_ign_video(self, response):
        sel2 = Selector(response)
        item = ItemLoader(Video(), sel2)
        item.add_xpath('titulo_v', '//h1/text()')
        item.add_xpath('fecha_v', '//span[@class="publish-date"]/text()')
 
        yield item.load_item()
 
    def parse_ign_new(self, response):
        sel3 = Selector(response)
        item = ItemLoader(Articulo(), sel3)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('contenido', '//h3/text()')
 
        yield item.load_item()