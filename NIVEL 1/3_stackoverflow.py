"""
OBJETIVO: 
    - Extraer las preguntas de la pagina principal de Stackoverflow con Scrapy
CREADO POR: LEONARDO KUFFO
ULTIMA VEZ EDITADO: 09 ENERO 2023
"""

# VER RECURSOS DE LA CLASE PARA INSTALAR SCRAPY
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
class Pregunta(Item):
    id = Field()
    pregunta = Field()
    descripcion = Field()

# CLASE CORE - SPIDER
class StackOverflowSpider(Spider):
    name = "MiPrimerSpider" # nombre, puede ser cualquiera 
    
    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }    

    # URL SEMILLA
    start_urls = ['https://stackoverflow.com/questions']


    # Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla
    def parse(self, response):
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response) 
        titulo_de_pagina = sel.xpath('//h1/text()').get()
        print (titulo_de_pagina)
        # Selector de varias preguntas
        preguntas = sel.xpath('//div[@id="questions"]//div[contains(@class,"s-post-summary ")]') 
        i = 0
        for pregunta in preguntas:
            item = ItemLoader(Pregunta(), pregunta) # Instancio mi ITEM con el selector en donde estan los datos para llenarlo

            # Lleno las propiedades de mi ITEM a traves de expresiones XPATH a buscar dentro del selector "pregunta"
            item.add_xpath('pregunta', './/h3/a/text()') 
            # item.add_xpath('descripcion', './/div[@class="s-post-summary--content-excerpt"]/text()')
            item.add_value('id', i)
            i += 1
            yield item.load_item() # Hago Yield de la informacion para que se escriban los datos en el archivo

# EJECUCION EN TERMINAL:
# scrapy runspider 3_stackoverflow.py -o resultados.csv -t csv