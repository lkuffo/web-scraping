from scrapy.item import Field
from scrapy.item import Item
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.loader import ItemLoader, Item
 
class Perfil(Item):
    autor = Field()
    opiniones = Field()
 
class TripAdvisor(CrawlSpider):
    name = "OpinionesTripAdvisor"
    custom_settings = {
        'USER_AGENT' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/44.0.2403.157 Safari/537.36",
        'CLOSESPIDER_PAGECOUNT' : 100
    }
 
    allowed_domains = ['tripadvisor.com.pe']
    start_urls = ['https://www.tripadvisor.com.pe/Hotels-g17181593-San_Borja_Lima_Region-Hotels.html']
 
    download_delay = 1
 
    rules = (
        #Paginacion de Hoteles
        # Rule(
        #     LinkExtractor(
        #         allow=r'-oa\d+-'
        #     ),follow=True
        # ),
        #Detalles de Hoteles
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_filtered_out_hotels_sponsored_0"]//a[@data-clicksource="HotelName"]']
            ),follow=True
        ),
        #Paginacion de Opiniones de un hotel
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ),follow=True,callback="parse_opinion"
        ),
    )
 
    def obtenerCalificacion(self,texto):
        calificacion = texto.split("_")[-1]
        return calificacion
    
 
    def parse_opinion(self,response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[contains(@class,"hotels-community-tab")]')
 
        for opinion in opiniones:
            # LLENANDO UN ITEM CON INFORMACION CUSTOMIZADA
            autor = {}
            autor["nombre"] = "Leonardo"
            autor["edad"] = 23

            # Llenando un arreglo dentro del ITEM
            opiniones = []
            opiniones.append("Opinion 1")
            opiniones.append("Opinion 2")

            item = Perfil(autor=autor, opiniones = opiniones)
 
            yield item
 