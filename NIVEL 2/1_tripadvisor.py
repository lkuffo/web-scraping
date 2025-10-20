"""
OBJETIVO: 
    - Extraer informacion sobre los hoteles de Guayaquil en TRIPADVISOR.
    - Aprender a realizar extracciones verticales utilizando reglas
    - Aprender a utilizar MapCompose para realizar limpieza de datos
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 19 OCTUBRE 2025
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose  # 2024: Nueva forma de importar MapCompose

class Hotel(Item):
    nombre = Field()
    score = Field() # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    descripcion = Field()
    amenities = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    # allowed_domains = ['tripadvisor.com']

    # Url semilla a la cual se hara el primer requerimiento
    # 2025: Ahora utilizaremos una version antigua de la pagina. Debido a que es otro dominio, tenemos que comentar la variable allowed_domains
    start_urls = ['https://web.archive.org/web/20230529051711/https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/Hotel_Review-' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_hotel"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    # Funcion a utilizar con MapCompose para realizar limpieza de datos
    def quitarDolar(self, texto):
        return texto.replace("$", "")

    # Callback de la regla
    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', '//span[@class="kJyXc P"]/text()',
                        MapCompose(self.quitarDolar)) # Debido a que ahora estamos obteniendo el score, no es necesario este post-procesamiento
        # Es posible utilizar Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas (lambda) en Python?
        item.add_xpath('descripcion', '//div[@class="_T FKffI TPznB Ci ajMTa Ps Z BB bmUTE"]/div/text()', # //text() nos permite obtener el texto de todos los hijos
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities',
                       '//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv
