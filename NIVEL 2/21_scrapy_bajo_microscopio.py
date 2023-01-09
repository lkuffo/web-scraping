"""
OBJETIVO: 
    - Aprender a utilizar el metodo para parsear las URL semilla en ves de aplicar reglas directamente
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 9 ENERO 2023
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader


class Hotel(Item):
    nombre = Field()
    score = Field() # El precio ahora carga dinamicamente. Por eso ahora obtenemos el score del hotel
    descripcion = Field()
    amenities = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class TripAdvisor(CrawlSpider):
    name = 'hotelestripadvisor'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        # 'FEED_EXPORT_FIELDS': ['id', 'descripcion', 'titular'], # Como ordenar las columnas en el CSV?
        # 'CONCURRENT_REQUESTS': 1 # numero de requerimientos concurrentes
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tripadvisor.com']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://www.tripadvisor.com/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    # No va a ser dos, va a ser 0.5 * download_delay hasta 1.5 * download delay
    # es decir, va a ser entre 1 y 3 segundos de una manera randomica. Ya es un comportamiento por defecto
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

    # EL RESPONSE ES EL DE LA URL SEMILLA
    def parse_start_url(self, response): 
        sel = Selector(response)
        hoteles = sel.xpath('.//div[@data-ttpn="Hotels_MainList"]')
        print("Numero de Resultados", len(hoteles))

    # Callback de la regla
    def parse_hotel(self, response):
        sel = Selector(response)

        item = ItemLoader(Hotel(), sel)
        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('score', './/div[@class="grdwI P"]/span/text()',
                        MapCompose(self.quitarDolar))
        # Utilizo Map Compose con funciones anonimas
        # PARA INVESTIGAR: Que son las funciones anonimas en Python?
        item.add_xpath('descripcion', '//div[@class="ssr-init-26f"]//div[@class="fIrGe _T"]//text()', # //text() nos permite obtener el texto de todos los hijos
                       MapCompose(lambda i: i.replace('\n', '').replace('\r', '')))
        item.add_xpath('amenities',
                       '//div[contains(@data-test-target, "amenity_text")]/text()')
        yield item.load_item()

# EJECUCION
# scrapy runspider 1_tripadvisor.py -o tripadvisor.csv -t csv
