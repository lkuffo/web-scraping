from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Propiedad(Item):
    nombre = Field()
    mts = Field()
    dorm = Field()
    ban = Field()
   
class PortalInmobiliario(CrawlSpider):

    name = "PortalInmobiliarioNivel2"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36',
        'METAREFRESH_ENABLED': False
    }

    start_urls = ['https://www.portalinmobiliario.com/venta/casa/punta-arenas-magallanes-y-antartica-chilena']   
    download_delay = 1
    rules = (
        Rule(
            LinkExtractor(
                allow = r'type=item'
            ),
            follow = True,
            callback = "parse_portal"
            ),
        )
    def parse_portal(self, response):
        sel = Selector(response)
        item = ItemLoader(Propiedad(), sel)
        item.add_xpath('nombre','//h1[@class="item-title__primary"]/text()')
        item.add_xpath('mts','//dd[@class="align-surface"]/text()')
        item.add_xpath('dorm','//dd[@class="align-room"]/text()')
        item.add_xpath('ban','//dd[@class="align-bathroom"]/text()')
        yield item.load_item()