from scraper.ElUniverso import ElUniversoSpider
from scrapy.crawler import CrawlerProcess

if __name__ == "__main__": # Código que se va a ejecutar al dar clic en RUN
    process = CrawlerProcess({
      'FEED_FORMAT': 'json',
      'FEED_URI': 'output.json'
    })
    process.crawl(ElUniversoSpider)
    process.start()