from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

def unir(item):
    valor = ''.join(item)
    try: 
        return float(valor)
    except:
        return valor
 
 
class detalle(Item):
    operacion = Field()
    precio = Field(
        output_processor=unir
    )
    parroquia = Field()
    referencia = Field()
    categoria = Field()
    hab = Field()
    parking = Field()
    banos = Field()
    superficie = Field()
    inmobiliaria = Field()
 
 
class inmobiliaria(CrawlSpider):
    name ="immoac"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 5  # Un poco alto
    }
    allowed_domains = ['immoac.com']
    #download_delay = 1
 
    #start_urls =['http://www.immoac.com/base/es/prod/Comprar/Andorra/--surface__0-34732--price__0-50000000_1.html']
    start_urls=['http://www.immoac.com/base/es/index.html',
                'http://www.immoac.com/base/es/prod/Alquilar_/Andorra/--surface__0-34732--price__0-50000000_1.html',
                'http://www.immoac.com/base/es/prod/Comprar_/Andorra/--surface__0-34732--price__0-50000000_1.html']
    rules = (
        Rule(
            LinkExtractor( #horizontalidad por tipo operacion
                allow=r'/prod/'
            ), follow=True),
 
        Rule(
            LinkExtractor( #horizontalidad por paginacion
                allow=r'-price__0-50000000_\d+'
            ), follow=True),
        Rule(
            LinkExtractor(  # horizontalidad por paginacion
                allow=r'zone_'
            ), follow=True),
        Rule(
            LinkExtractor( #verticalidad
                allow='Alquilar'
            ), follow=True, callback='parse_anuncio'),
        # verticalidad articulo
        Rule(
            LinkExtractor(
                allow=r'Comprar'
            ), follow=True, callback='parse_anuncio'),
    )
 
    def quitarcaract(self,texto):
        nuevoTexto=texto.replace('\n', '').replace('\r','').replace(' m','').replace('&nbsp;','').strip()
        return nuevoTexto
 
    def limpiarTexto(self, texto):
        nuevoTexto = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('http://www.', '').strip()
        return nuevoTexto
    def textoanumero(self, texto):
        numero = int(texto)
        return numero
    def limpiarprecio(self, texto):
        nuevoTexto = texto.replace('\n', '').replace('\r', '').replace(' m', '').replace(',', '').strip()
        #nuevoTexto= float(nuevoTexto)
        return nuevoTexto
    def limpiarsuperficie(self, texto):
        nuevoTexto = int(texto.replace('\n', '').replace('\r', '').replace(' m', '').replace(',', '').strip())
        return nuevoTexto
    def parse_anuncio(self, response):
        sel = Selector(response)
        item = ItemLoader(detalle(), sel)
 
        item.add_value('inmobiliaria', 'Immoac') #add_value me sirve para establecer un parametro fijo.
        #item.add_xpath('inmobiliaria','//div[@class="brand"]/a/@*', MapCompose(self.limpiarTexto))
        item.add_xpath('categoria', '//span[@class="text-primary"]/../text()')
        item.add_xpath('operacion','//span[@class="text-primary"]/text()',
                       MapCompose(self.quitarcaract))
        item.add_xpath('precio',
                       '//h1[@class="price average-color col-xs-12 col-sm-12 col-md-12 text-center  pull-right  padding3"]/span/text()',
                       MapCompose(self.limpiarprecio))
        item.add_xpath('parroquia', '//i[@class="fa fa-map-marker fa-lg"]/../../text()')
 
        item.add_xpath('referencia', '//div[@class=" col-md-8"]/h2[2]/text()',
                       MapCompose(self.quitarcaract))
        item.add_xpath('hab',
                       '//div[@class="col-xs-10 col-sm-10 col-md-10 text-primary nowrap"]/following-sibling::div/h2/text()',
                       MapCompose(self.textoanumero))
        item.add_xpath('banos','//i[@class="fa fa-tint"]/../../following-sibling::div/h2/text()',
                       MapCompose(self.textoanumero))
 
        item.add_xpath('parking', '//i[@class="fa fa-car"]/../../following-sibling::div/h2/text()')
        item.add_xpath('superficie', '//h2[contains(text(), "Sup. Total")]/../following-sibling::div/h2/text()',
                       MapCompose(self.limpiarsuperficie))
 
        yield item.load_item()
 