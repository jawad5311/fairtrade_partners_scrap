
import scrapy

from scrapy_selenium import SeleniumRequest


class PartnerDirSpider(scrapy.Spider):
    name = 'partner_dir'
    allowed_domains = ['fairtradecertified.org']
    start_urls = ['https://partner.fairtradecertified.org/directory/results']

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse
        )

    def parse(self, response):
        print(response)
        print(response.meta)
        
