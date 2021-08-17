from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
 
# ABSTRACCION DE DATOS A EXTRAER - DETERMINA LOS DATOS QUE TENGO QUE LLENAR Y QUE ESTARAN EN EL ARCHIVO GENERADO
class HorarioOnibusRecife(Item):
    nomeRota = Field()
    #diaUtil = Field()
    #horarioUtil = Field()
    #sabado = Field()
    #horarioSabado = Field()
    #domingo = Field()
    #horarioDomingo = Field()
 
 
# CLASE CORE - Al querer hacer extraccion de multiples paginas, heredamos de CrawlSpider
class ToNoPonto(CrawlSpider):
    name = "Horarios"
 
    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }
 
    # Url semilla a la cual se hara el primer requerimiento
    start_urls=["http://tonoponto.com/itinerario-horarios-de-onibus/pe-recife-grande-recife/"]
 
    # Tiempo de espera entre cada requerimiento. Nos ayuda a proteger nuestra IP.
    download_delay = 2
 
    # Reduce el espectro de busqueda de URLs. No nos podemos salir de los dominios de esta lista
    allowed_domains = ['tonoponto.com']
 
    # Tupla de reglas para direccionar el movimiento de nuestro Crawler a traves de las paginas
    rules = (
        Rule(# Regla de movimiento VERTICAL hacia el detalle de las linhas de ônibus
            LinkExtractor(
                allow=r'/pe-grande-recife-' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback='parse_horario'), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )
 
 
    # Callback de la regla
    def parse_horario (self, response):
        sel = Selector(response)
        item = ItemLoader (HorarioOnibusRecife(), sel)
 
        item.add_xpath('nomeRota', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                                   '@class="mainContentWrapper"/h1/text()')
        #item.add_xpath('diaUtil', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                              #'@class="mainContentWrapper"/div[@class="mainContent"]/p[1][@class="title_p"/text()')
        #item.add_xpath('horarioUtil', '//@div[class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                              #'@class="mainContentWrapper"/div[@class="mainContent"]/ul[1][@class="listaHorarios"/text()')
        #item.add_xpath('sabado', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                                  #'@class="mainContentWrapper"/div[@class="mainContent"]/p[2][@class="title_p"/text()')
        #item.add_xpath('horarioSabado', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                                      #'@class="mainContentWrapper"/div[@class="mainContent"]/ul[2][@class="listaHorarios"/text()')
        #item.add_xpath('domingo', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                                  #'@class="mainContentWrapper"/div[@class="mainContent"]/p[3][@class="title_p"/text()')
        #item.add_xpath('horarioDomingo', '//div[@class="col-lg-9 col-md-8 col-sm-12 col-xs-12"]/div['
                                      #'@class="mainContentWrapper"/div[@class="mainContent"]/ul[3][@class="listaHorarios"/text()')
 
        yield item.load_item()