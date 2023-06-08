from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
 
class acceso(Item):
 
    TodosServicioDiscapacitados = Field()
    barrasWc = Field()
    adaptadoParaSillasDeRuedas = Field()
    accessoASillasDeRuedas = Field()
    ingles = Field()
 
 
class HotelCrawler(Spider):
    name = "pruebaHotel"
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36'
    }    
 
    start_urls = ['https://www.booking.com/hotel/pf/intercontinental-tahiti-resort.es.html?aid=2046495&label=gen173nr-1FCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQuIAgGoAgO4ArqcroAGwAIB0gIkZTdhODY3MzAtODg0Ni00YzEyLWI4ZDctNWM3NDFmYWU5Zjhl2AIG4AIB&sid=6e8a8d5c36b596a1a011bb442a0b00ff&stid=304142&dest_id=3976&dest_type=region&dist=0&group_adults=2&group_children=0&hapos=2&hpos=2&lang=es&nflt=class%3D5%3Bclass%3D4%3Bhotelfacility%3D25%3B&no_rooms=1&room1=A%2CA&sb_price_type=total&soz=1&sr_order=popularity&srepoch=1611414829&srpvid=eeac6b16b99b0044&type=total&ucfs=1&lang_click=other;cdl=fr;lang_changed=1',
                  'https://www.booking.com/hotel/pf/manava-suite-resort-tahiti.es.html?aid=2046495&label=gen173nr-1FCAEoggI46AdIM1gEaEaIAQGYAQq4ARfIAQzYAQHoAQH4AQuIAgGoAgO4ArqcroAGwAIB0gIkZTdhODY3MzAtODg0Ni00YzEyLWI4ZDctNWM3NDFmYWU5Zjhl2AIG4AIB&sid=6e8a8d5c36b596a1a011bb442a0b00ff&stid=304142&dest_id=3976&dest_type=region&dist=0&group_adults=2&group_children=0&hapos=3&hpos=3&lang=es&nflt=class%3D5%3Bclass%3D4%3Bhotelfacility%3D25%3B&no_rooms=1&room1=A%2CA&sb_price_type=total&soz=1&sr_order=popularity&srepoch=1611414829&srpvid=eeac6b16b99b0044&type=total&ucfs=1&lang_click=other;cdl=fr;lang_changed=1']
 
 
    def parse(self, response):
        item = ItemLoader(acceso(), response)
 
        item.add_xpath('TodosServicioDiscapacitados', '//div[@data-section-id="19"]//li//text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('barrasWc', '//*[@data-name-en="toilet with grab rails"]//text', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('adaptadoParaSillasDeRuedas', '//*[@data-name-en="property is wheel chair accessible"]/parent::*//text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('accessoASillasDeRuedas', '//*[@data-name-en="property is wheel chair accessible"]/parent::*//text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('ingles', '//div[@class="facilitiesChecklistSection"][last()]//li[contains(text(),"English")]/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
 
 
        yield item.load_item()
 
# EJECUCION EN TERMINAL:
# scrapy runspider 24_booking.py -o resultados.csv -t csv