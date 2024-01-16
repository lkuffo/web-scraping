from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Articulo(Item):
    nit=Field()
    nombre=Field()
    actividad = Field()
    direccion=Field()
    ciudad=Field()
    departamento=Field()
    telefono=Field()
    
class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
 
    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
          }
 
   
    start_urls = ['https://directorio-empresas.einforma.co/actividad/6810-actividades-inmobiliarias-realizadas-con-bienes-propios-o-arrendados/?qPg=1']
    
    allowed_domains = ['directorio-empresas.einforma.co']
    download_delay = 1
 
    # Tupla de reglas
    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'qPg=\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
            Rule( # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=r'/informacion-empresa/' 
            ), follow=True, callback='parse_items'), # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )
 
    def parse_items(self, response):
 
        item = ItemLoader(Articulo(), response)
        
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        
        item.add_xpath('nit','//table[@class="informe"]//a[@href="#formularioRegistro"]//text()')
        item.add_xpath('nombre','//h2[@class="title04 mt5"]//text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').replace(' ', '').strip()))
        item.add_xpath('actividad','//table[@class="informe"]//tr[3]//td[2]/text()')
        item.add_xpath('direccion','//span[@class="street-address"]//text()')
        item.add_xpath('ciudad','//span[@class="locality"]//text()')
        item.add_xpath('departamento','//span[@id="situation_prov"]//text()')
        item.add_xpath('telefono','//span[@class="lh1-5"]//text()')
        
 
        yield item.load_item()
