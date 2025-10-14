from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader

# Quiero extraer de la tabla que aparece en el perfil de cada atleta en BJJ Heroes:
class Fila_df(Item):
    opponent = Field()
    win_loss = Field()
    method = Field()
    tournament = Field()
    weight = Field()
    stage = Field()
    year = Field()
   
# Defino el spider y la url semilla / Defino el user_agent:
class bjj_heroes_spider(Spider):
    name = "BJJHeroesScraper" # nombre, puede ser cualquiera
    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }   
    # URL SEMILLA
    start_urls = ['https://www.bjjheroes.com/bjj-fighters/marcio-cruz']

# Funcion que se va a llamar cuando se haga el requerimiento a la URL semilla
    def parse(self, response):
        # Selectores: Clase de scrapy para extraer datos
        sel = Selector(response)
        # Selector de la tabla a la que quiero ir a buscar la info:
        lineas = sel.xpath('//tbody//tr')
        for linea in lineas:
            item = ItemLoader(Fila_df(),linea)
            item.add_xpath('opponent','.//td[2]/span/text()')
            item.add_xpath('win_loss','.//td[3]/text()')
            item.add_xpath('method','.//td[4]/text()')
            item.add_xpath('tournament','.//td[5]/text()')
            item.add_xpath('weight','.//td[6]/text()')
            item.add_xpath('stage','.//td[7]/text()')
            item.add_xpath('year','.//td[8]/text()')
            yield item.load_item()