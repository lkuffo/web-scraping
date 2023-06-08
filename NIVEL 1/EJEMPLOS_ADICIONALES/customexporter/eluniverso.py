"""
OBJETIVO: 
    - Extraer los titulares y el resumen de las noticias en la pagina principal de deportes de EL UNIVERSO.
    - Contrastar el uso de Beautiful Soup y Scrapy para parsear el arbol HTML.
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 12 ABRIL 2020
"""

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from exportador import CustomCSVExporter

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
class Noticia(Item):
    id = Field()
    titular = Field()
    descripcion = Field()


# CLASE CORE - SPIDER  
class ElUniversoSpider(Spider):
    name = "MiSegundoSpider"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'FEED_EXPORTERS': {
            'csv': 'exportador.CustomCSVExporter.CsvCustomSeperator'
        }
        # 'FEED_EXPORT_FIELDS': ['id', 'descripcion', 'titular'] # Como ordenar las columnas en el CSV?
    }
    start_urls = ['https://www.eluniverso.com/deportes']

    def parse(self, response):
        sel = Selector(response)
        noticias = sel.xpath('//div[@class="view-content"]/div[@class="posts"]')
        for i, elem in enumerate(noticias): # PARA INVESTIGAR: Para que sirve enumerate?
            item = ItemLoader(Noticia(), elem) # Cargo mi item

            # Llenando mi item a traves de expresiones XPATH
            item.add_xpath('titular', './/h2/a/text()')
            item.add_xpath('descripcion', './/p/text()')
            item.add_value('id', i)
            yield item.load_item() # Retorno mi item lleno


        # METODO #2: UTILIZANDO BEAUTIFUL SOUP => En este caso aumenta un poco la complejidad

        # soup = BeautifulSoup(response.body)
        # contenedor_noticias = soup.find_all(class_='view-content')
        # id = 0
        # for contenedor in contenedor_noticias:
        #   noticias = contenedor.find_all(class_='posts', recursive = False)
        #   for noticia in noticias:
        #     item = ItemLoader(Noticia(), response.body)
        #     titular = noticia.find('h2').text.replace('\n', '').replace('\r', '')
        #     descripcion = noticia.find('p')
        #     if (descripcion):
        #       item.add_value('descripcion', descripcion.text.replace('\n', '').replace('\r', ''))
        #     else:
        #       item.add_value('descripcion', 'N/A')
        #     item.add_value('titular', titular)
        #     item.add_value('id', id)
        #     id += 1
        #     yield item.load_item()

# EJECUCION
# scrapy runspider 4_eluniverso.py -o resultados.csv -t csv