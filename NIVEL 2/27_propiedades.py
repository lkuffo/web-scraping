from scrapy.item import Field

from scrapy.item import Item

from scrapy.spiders import CrawlSpider, Rule

from scrapy.selector import Selector

from scrapy.loader.processors import MapCompose

from scrapy.linkextractors import LinkExtractor

from scrapy.loader import ItemLoader





class Propiedades(Item):

    id_ = Field()

    nombre = Field()

    link= Field()

    precio = Field()

    estimado_pago = Field()

    total_precio = Field()

    precio_m2= Field()

    recamaras = Field()

    sanitario = Field()

    tam_construccion = Field()

    estacionamiento = Field()

    antiguedad = Field()

    pisos = Field()

    servicios = Field()

    terraza = Field()

    cisterna = Field()

    alberca = Field()

    gimnasio = Field()

    mascotas = Field()

    telefonia = Field()

    gas_natural = Field()

    cuarto_servicio = Field()

    lavanderia = Field()

    zona_privada = Field()

    seguridad_privada = Field()

    aire = Field()

    descripcion = Field()

    link = Field()

   







class Inmuebles(CrawlSpider):

    name = 'propiedades.com'

    custom_settings = {

        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',

        'CLOSESPIDER_PAGECOUNT':100,

        'FEED_EXPORT_ENCODING': 'iso-8859-1'

    }



   

    allowed_domains = ['propiedades.com']



   

    start_urls = ['https://propiedades.com/yucatan/casas-venta']



   

    download_delay = 1



   

    rules = (

        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles

            LinkExtractor(

                allow=r'/inmuebles/casa-en-venta-',

            ), follow=True, callback="parse_item"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs

    )







    # Callback de la regla

    def parse_item(self, response):

        sel = Selector(response)

   

           

        item = ItemLoader(Propiedades(), sel)

        item.add_xpath('id_','//li[@data-value="2" ]/text()')

        item.add_xpath('link','//div[@class="hidden"]/text()')

        item.add_xpath('nombre', '//p[@class="label-type-property"]/text()')

        item.add_xpath('precio', '//span[@class="label-cantidad-credimejora"]/text()')

        item.add_xpath('estimado_pago', '//span[@class="label-title-credimejora"]/text()')

        item.add_xpath('total_precio','//span[@class="price"]/text()')

        item.add_xpath('precio_m2', '//p[@class="txt-average-price"]/text()')

        item.add_xpath('recamaras','//span[text()="Recámaras"]/following-sibling::span/text()')

        item.add_xpath('sanitario','//span[text()="Baños "]/span[1]/text()')

        item.add_xpath('tam_construccion','//i[@class="icon-tamano-construccion"]/following-sibling::span[last()]/text()')

        item.add_xpath('estacionamiento','//i[@class="icon-estacionamiento"]/following-sibling::span[last()]/text()')

        item.add_xpath('antiguedad','//i[@class="icon-antiguedad"]/following-sibling::span[last()]/text()')

        item.add_xpath('pisos','//i[@class="icon-niveles"]/following-sibling::span[last()]/text()')

        item.add_xpath('servicios','//i[@class="icon-servicio"]/following-sibling::span[1]/text()')

        item.add_xpath('terraza','//span[text()="Terraza"]/text()')

        item.add_xpath('cisterna','//span[text()="Cisterna"]/text()')

        item.add_xpath('alberca','//span[text()="Alberca"]/text()')

        item.add_xpath('gimnasio','//span[text()="Gimnasio"]/text()')

        item.add_xpath('mascotas','//span[text()="Mascotas"]/text()')

        item.add_xpath('telefonia','//span[text()="Telefonía"]/text()')

        item.add_xpath('gas_natural','//span[text()="Gas Natural"]/text()')

        item.add_xpath('cuarto_servicio','//span[text()="Cuarto de servicio"]/text()')

        item.add_xpath('lavanderia','//span[text()="Lavandería"]/text()')

        item.add_xpath('seguridad_privada','//span[text()="Seguridad privada"]/text()')

        item.add_xpath('zona_privada','//span[text()="Zona privada"]/text()')

        item.add_xpath('aire','//span[text()="Aire acondicionado"]/text()')

        item.add_xpath('descripcion', '//div[@class="subsection-content"]/p/text()')

       

       

    

        #obtener los links de cada propiedad que se le hace scraping

        link = sel.xpath('./a/@href').extract()

        link_text = sel.xpath('./a/text()').extract()

        item.add_xpath('link',link_text)

       

         

        yield item.load_item()

