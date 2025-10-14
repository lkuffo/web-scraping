from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Pelicula(Item):
    titulo = Field()
    fecha = Field()
    nacionalidad = Field()
 
class SensacineCrawler(CrawlSpider):
    name = 'Sensacine'
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 40
    }
 
    download_delay = 1
 
    allowed_domains = ['allocine.fr']
 
    start_urls = ['http://www.allocine.fr/societe/fichesociete-3872/activite-8030/']
 
    rules = (
        #paginacion
        Rule(
           LinkExtractor(
                   allow=r'/?page='
           ), follow=True
        ),
        #detalles
        Rule(
            LinkExtractor(
                allow=r'/fichefilm_gen_cfilm='
            ), follow=True, callback='parse_items'
        ),
    )

    def parsearFecha(self, fecha):
        fechaFormateada = ""
        fecha = fecha.strip() # elimino espacio al inicio y al final de la cadena
        dia, mes, anio = fecha.split(' ') # divido la cadena en 3 y asigno a las 3 variables
        mapeoMeses = {
            'mars': '03',
            'octobre': '10',
            'juin': '06'
            # Llenar con todos los meses...
        }
        mesEspanol = mapeoMeses[mes] # Mapeo el mes en frances al mes en numeros
        fechaFormateada = dia + "/" + mesEspanol + "/" + anio[-2:] # Armo el formato que quiero concatenando cadenas
        return fechaFormateada
 
    def parse_items(self, response):
        item = ItemLoader(Pelicula(), response)
        item.add_xpath('titulo', '//div[@class="titlebar-title titlebar-title-lg"]/text()')
        item.add_xpath('fecha', '//span[contains(@class,"date blue-link")]/text()', MapCompose(parsearFecha)) # MapCompose VER VIDEO TRIP ADVISOR PT2
        item.add_xpath('nacionalidad', '//span[contains(@class,"nationality")]/text()')
 
        yield item.load_item()