
import scrapy

from scrapy_selenium import SeleniumRequest


class PartnerDirApiSpider(scrapy.Spider):
    name = 'partner_dir_api'
    allowed_domains = ['fairtradecertified.org']
    start_urls = ['https://partner.fairtradecertified.org/directory/account/get?hasProfile=false&page=1&perPage=100']
    page_num = 1

    def parse(self, response):
        profiles = response.json()['accounts']
        for profile in profiles:
            name = profile['Marketing_Display_Name__c']
            country = profile['BillingCountry']
            ftusa_id = profile['FLO_ID__c']
            flo_id = profile['FLO_ID_Supplier__c']
            account_type = profile['Account_Type__c']
            marketing_cat = profile['Account_Marketing_Categories__c']
            profile_url = profile['Slug']

            if profile_url:
                url = f'https://partner.fairtradecertified.org/profile/{profile_url}'
                yield SeleniumRequest(
                    url=url,
                    callback=self.parse_profile,
                    meta={
                        'name': name,
                        'country': country,
                        'ftusa_id': ftusa_id,
                        'flo_id': flo_id,
                        'account_type': account_type,
                        'marketing_cat': marketing_cat,
                }
                )
            # else:
            #     yield {
            #         'name': name,
            #         'country': country,
            #         'ftusa_id': ftusa_id,
            #         'flo_id': flo_id,
            #         'account_type': account_type,
            #         'marketing_cat': marketing_cat,
            #     }

        # if profiles:
        #     self.page_num += 1
        #     print('PAGE NUMBER: ', self.page_num)
        #     next_url = f'https://partner.fairtradecertified.org/directory/account/get?hasProfile=false&page={self.page_num}&perPage=100'
        #     yield scrapy.Request(
        #         url=next_url,
        #         callback=self.parse
        #     )

    @staticmethod
    def parse_profile(response):
        driver = response.meta['driver']
        sel = response.replace(body=driver.page_source)
        print('PROFILE NAME: ', sel.css('.profile-name::text').get())

