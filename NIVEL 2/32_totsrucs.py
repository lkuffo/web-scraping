from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Capitol(Item):
    titol = Field()
    url = Field()
 
class TotsRucs(CrawlSpider):
 
    name = "Capitols"
    custom_settings = {
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    start_urls = ['https://web.totsrucs.cat/index.php?pagina=elinks&veure=temporada&id=7164']
 
    download_delay = 2
 
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/index.php\?pagina=elinks&veure=elink&id='
            ), follow=True, callback="parse_elink"
        ),
    )
 
    def parse_elink(self, response):
        sel = Selector(response)
        item = ItemLoader(Capitol(), sel)
 
        item.add_xpath('titol', '//div[@id="contingut"]/a/text()')
        item.add_xpath('url', '//div[@id="contingut"]/a/@href')
 
        yield item.load_item()