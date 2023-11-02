"""
OBJETIVO: 
    - Solidificar los conocimientos de Scrapy
    - Llenar el item con .add_value
    - Aprender el uso de .get() y .getall() para obtener información de la página
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 05 AGOSTO 2023
"""
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    titulo = Field()
    citaciones = Field() 
    autores = Field()
    url = Field()

# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class GoogleScholar(CrawlSpider):
    name = 'googlescholar'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'DEPTH_LIMIT': 1, # Para definir que solo se vaya a un nivel de profundidad
        'FEED_EXPORT_ENCODING': 'utf-8' # Para evitar problemas con codificacion de simbolos
    }

    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['scholar.google.com']

    # Url semilla a la cual se hara el primer requerimiento
    start_urls = ['https://scholar.google.com/scholar?as_ylo=2023&q=AI&hl=en&as_sdt=0,5']

    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2

    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule( # Regla de movimiento VERTICAL hacia las citaciones de dicho articulo
            LinkExtractor(
                restrict_xpaths='.//div[@class="gs_fl gs_flb"]'
                #allow=r'\?cites=' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_start_url"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    def parse_start_url(self, response):
        sel = Selector(response)

        # Obtenemos todos los articulos 
        articulos = sel.xpath('.//div[@class="gs_ri"]')

        for articulo in articulos:
            item = ItemLoader(Articulo(), articulo)

            # Extraemos el titulo
            # Hacemos .getall() debido a que el texto del titulo puede venir dentro de varios
            # tags dentro del <a>
            titulo = articulo.xpath('.//h3/a//text()').getall()
            titulo = "".join(titulo) # .getall() nos devuelve una lista de textos; que podemos unir

            # Obtenemos la URL del articulo
            url = articulo.xpath('.//h3/a/@href').get()

            # Obtenemos los autores del articulo
            autores = articulo.xpath('.//div[@class="gs_a"]//text()').getall()
            autores = "".join(autores)
            autores = autores.split('-')[0].strip()

            # Intentamos obtener el numero de citaciones (ya que no siempre existirá)
            # Por eso inicializamos el valor de la variable en 0 
            citaciones = 0
            try:
                citaciones = articulo.xpath('.//div[@class="gs_fl gs_flb"]/a[contains(@href, "cites")]/text()').get()
                citaciones = citaciones.replace('Cited by ', '')
            except:
                pass

            # Llenamos el Item
            item.add_value('titulo', titulo)
            item.add_value('citaciones', citaciones)
            item.add_value('url', url)
            item.add_value('autores', autores)
            yield item.load_item()

# EJECUCION
# scrapy runspider 7_googlescholar.py -o articulos.csv
