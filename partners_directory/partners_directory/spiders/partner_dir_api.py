import scrapy


class PartnerDirApiSpider(scrapy.Spider):
    name = 'partner_dir_api'
    allowed_domains = ['fairtradecertified.org']
    start_urls = ['https://partner.fairtradecertified.org/directory/account/get?hasProfile=false&page=1&perPage=100']

    def parse(self, response):
        profiles = response.json()['accounts']
        for profile in profiles:
            print(profile['Marketing_Display_Name__c'])
        


