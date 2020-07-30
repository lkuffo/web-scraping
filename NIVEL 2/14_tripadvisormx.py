from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Opinion(Item):
    titulo = Field()
    calificacion = Field()
    contenido = Field()
    autor = Field()
 
class TripAdvisor(CrawlSpider):
    name = 'Opiniones'
    custom_settings = {  # para que no te identifique como robot
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 100
    }
 
    allowed_domains = ['tripadvisor.com', 'tripadvisor.com.mx']
    start_urls = ['https://www.tripadvisor.com.mx/Hotels-g2048993-Tepatitlan_de_Morelos-Hotels.html']
    download_delay = 1
 
    # rules define a dónde puede o no pueder ir el crawler
    rules = (
        #paginación de hoteles (horizontal)
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-' # \d+ es para que permita cualquier número
            ), follow=True
        ),
        #detalle de hoteles (vertical)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths = ['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="HotelName"]'] #limitar el espectro de búsqueda
            ), follow=True
        ),
        #paginacion de opiniones (horizontal)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        #detalle de perfil de usuario (vertical)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]//a[contains(@class,"ui_header")]']
            ), follow=True, callback='parse_opinion'
        )
    )
 
    def obtenerCalificacion(self,texto):
        calificacion = texto.split("_")[-1]
        return calificacion
 
 
    def parse_opinion(self, respose):
        sel = Selector(respose)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get() #el linkextractor está dentro del perfil de usuario, así que el autor se sabe antes de correr el itemloader
 
        for opinion in opiniones:
            item = ItemLoader(Opinion(),opinion)
            item.add_value('autor', autor)
            item.add_xpath('titulo', './/div[@class="_3IEJ3tAK _2K4zZcBv"]/text()')
            item.add_xpath('contenido', './/q/text()')
            item.add_xpath('calificacion', './/div[@class="_1VhUEi8g _2K4zZcBv"]/span/@class',
                           MapCompose(self.obtenerCalificacion))
 
 
        yield item.load_item()