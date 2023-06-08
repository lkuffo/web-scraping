from scrapy.item import Field, Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup
from middlewares import CustomProxyMiddleware


class SpiderCuevana(CrawlSpider):
  name = 'Cuevana_cinehogares'
  custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
      'LOG_ENABLED': False,
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'CLOSESPIDER_PAGECOUNT': 92,
      'CONCURRENT_REQUESTS': 1,
      'DEPTH_PRIORITY': 1,
      'SCHEDULER_DISK_QUEUE': 'scrapy.squeues.PickleFifoDiskQueue',
      'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
      'DOWNLOADER_MIDDLEWARES': {            
        'middlewares.CustomProxyMiddleware.CustomProxyMiddleware': 350,            
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400,        
      }
  }
  download_delay = 1

  allowed_domains = ['cuevana3.io']
  start_urls = ['https://cuevana3.io/peliculas/page/1', 'https://cuevana3.io/peliculas/page/2']

  rules = (
      Rule(
          LinkExtractor(
              allow=r'cuevana3.io/\d+/',
              tags='a',
              attrs='href',
              restrict_xpaths='//li[@class="xxx TPostMv"]//a',
          ), follow=True, callback='GetLink'),
  )

  def GetLink(self, response):
    print(response)