import scrapy
from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
 
 
 
class Inmueble(Item):
    inmueble = Field()
    valor = Field()
    area = Field()
    numero_Hab = Field()
 
 
class Finca_Raiz(Spider):
    name = "Mispider"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
    }
 
    start_urls = ['https://www.fincaraiz.com.co/proyectos-vivienda-nueva/']
 
    def parse(self,response):
        sel = Selector(response)
        inmuebles = sel.xpath('//div[@id="divAdverts"]//ul[contains(@id,"rowIndex_")]')   
        for inmueble in inmuebles:
            item = ItemLoader(Inmueble(), inmueble)
            item.add_xpath('inmueble', './/div[@class="span-title"]/a/div/b/text()')
            item.add_xpath('valor', './/li[@class = "price"]/text()') 
 
            yield item.load_item() 