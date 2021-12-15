import scrapy


class PartnerDirSpider(scrapy.Spider):
    name = 'partner_dir'
    allowed_domains = ['test.com']
    start_urls = ['http://test.com/']

    def parse(self, response):
        pass
