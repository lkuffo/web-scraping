import cloudscraper
from scrapy.http import HtmlResponse
import logging

class CustomCloudflareMiddleware(object):

    cloudflare_scraper = cloudscraper.create_scraper()

    def process_response(self, request, response, spider):
        request_url = request.url
        response_status = response.status
        if response_status not in (403, 503):
            return response
        
        spider.logger.info("Cloudflare detected. Using cloudscraper on URL: %s", request_url)
        cflare_response = self.cloudflare_scraper.get(request_url)
        cflare_res_transformed = HtmlResponse(url = request_url, body=cflare_response.text, encoding='utf-8')
        return cflare_res_transformed