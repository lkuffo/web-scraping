from scrapy.item import Field 
from scrapy.item import Item 
from scrapy.spiders import CrawlSpider, Rule 
from scrapy.selector import Selector 
from scrapy.loader.processors import MapCompose 
from scrapy.linkextractors import LinkExtractor 
from scrapy.loader import ItemLoader 
from bs4 import BeautifulSoup

def obtenerPagina(button_id):
  button_id = button_id.split('/')[-1]
  numero = ''.join([s for s in button_id if s.isdigit()])
  if len(numero) == 0 or len(numero) > 3:
    return None
  url_base = "https://www.falabella.com/falabella-cl/category/cat3112/Perfumes-hombre?page="
  return url_base + str(numero[0])

class Articulo(Item):     
  color = Field()  
  
class falabella(CrawlSpider):     
  name = 'falabella'     
  custom_settings = {         
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/80.0.3987.149 Safari/537.36',          
    'CLOSESPIDER_PAGECOUNT': 100 # Numero maximo de paginas en las cuales voy a descargar items. Scrapy se cierra cuando alcanza este numero     
  }     
  
  #Restringir mi rango de busqueda en las paginas, que no vayan a paginas que no pertenecen a este dominio     
  allowed_domains = ['falabella.com']     
  start_urls = ['https://www.falabella.com/falabella-cl/category/cat3112/Perfumes-hombre']      
  
  download_delay = 0.3 
  
  rules = ( 
    #Paginacion         
    Rule(             
      LinkExtractor(                 
        tags=('button',),
        attrs=('id',),
        process_value=obtenerPagina
      ), follow=True
    ),
    #Detalle de productos         
    Rule(             
      LinkExtractor( 
        allow=r'/product/'
      ), follow=True, callback="parse_item"
    ),
  )     
  
  def parse_item(self, response):         
    item = ItemLoader(Articulo(), response)          
    item.add_xpath('color', '//span[@class="copy3 primary  jsx-185326735 normal   "]/text()')
    yield item.load_item()