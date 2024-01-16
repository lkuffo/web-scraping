from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
    imagen = Field()
 
 
class Mercadolibre(CrawlSpider):
    name = "Scrap-MercadoLibre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 10
    }
 
    download_delay = 2
 
    allowed_domains = ["listado.mercadolibre.com.ve", "articulo.mercadolibre.com.ve", "mercadolibre.com.ve"]
 
    start_urls = ["https://listado.mercadolibre.com.ve/perros#D[A:perros]"]
 
    rules = (
        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'/_Desde_\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ),follow=True
        ),
        # Detalles de los productos
        Rule(
            LinkExtractor(
                allow=r'/MLV-'
            ), follow=True, callback='parse_items'
        ),
    )
 
    def Limpiartext(self, texto):
        nuevotext = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevotext
 
    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)
        item.add_xpath('titulo', '//h1/text()', MapCompose(self.Limpiartext))
        item.add_xpath('precio', '//span[@class="andes-money-amount__fraction"]/text()')
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(self.Limpiartext))
        item.add_xpath('imagen', '//img[@class="ui-pdp-image ui-pdp-gallery__figure__image" and @data-index="0"]/@src')
 
        yield item.load_item()