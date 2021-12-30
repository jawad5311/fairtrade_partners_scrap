
# module imports
import scrapy
from scrapy.loader import ItemLoader

# local import
from ..items import PartnersDirectoryItem


class PartnerDirApiSpider(scrapy.Spider):
    name = 'partner_dir_api'
    allowed_domains = ['fairtradecertified.org']
    start_urls = ['https://partner.fairtradecertified.org/directory/account/get?hasProfile=false&page=1&perPage=100']
    page_num = 1

    def parse(self, response):
        # converting response into json and grabbing profiles
        profiles = response.json()['accounts']
        for profile in profiles:
            title = profile['Marketing_Display_Name__c']
            country = profile['BillingCountry']
            ftusa_id = profile['FLO_ID__c']
            flo_id = profile['FLO_ID_Supplier__c']
            account_cat = profile['Account_Type__c']
            marketing_cat = profile['Account_Marketing_Categories__c']

            # if profile link available then parse profile
            profile_available = profile['Slug']
            if profile_available:
                account_id = profile['AccountId']  # profile id use to create absolute link
                url = f'https://partner.fairtradecertified.org/profile/get/{account_id}'
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_profile,
                    # transferring previous scrapped data as metadata
                    meta={
                        'title': title,
                        'country': country,
                        'ftusa_id': ftusa_id,
                        'flo_id': flo_id,
                        'account_cat': account_cat,
                        'marketing_cat': marketing_cat
                    })
            else:
                # load data into relevant item fields
                l = ItemLoader(item=PartnersDirectoryItem())
                l.add_value('title', title)
                l.add_value('country', country)
                l.add_value('account_cat', account_cat)
                l.add_value('marketing_cat', marketing_cat)
                l.add_value('ftusa_id', ftusa_id)
                l.add_value('flo_id', flo_id)
                l.add_value('website', '')
                l.add_value('phone', '')
                l.add_value('email', '')
                yield l.load_item()

        # Handling pagination
        if profiles:
            self.page_num += 1  #
            print('PAGE NUMBER: ', self.page_num)
            next_url = f'https://partner.fairtradecertified.org/directory/account/get?hasProfile=false&page={self.page_num}&perPage=100'
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )

    @staticmethod
    def parse_profile(response):
        l = ItemLoader(item=PartnersDirectoryItem())

        # converting scrapy response into json
        data = response.json()

        # Grabbing data from metadata
        title = response.meta['title']
        country = response.meta['country']
        ftusa_id = response.meta['ftusa_id']
        flo_id = response.meta['flo_id']
        account_cat = response.meta['account_cat']
        marketing_cat = response.meta['marketing_cat']

        # Grabbing data from the json
        email = data['profile'].get('General_Contact_E_mail__c')
        phone = data['profile'].get('General_Contact_Phone_Number__c')
        website = data['account'].get('Website')

        # loading data into relevant item fields
        l.add_value('title', title)
        l.add_value('country', country)
        l.add_value('account_cat', account_cat)
        l.add_value('marketing_cat', marketing_cat)
        l.add_value('ftusa_id', ftusa_id)
        l.add_value('flo_id', flo_id)
        l.add_value('website', website)
        l.add_value('phone', phone)
        l.add_value('email', email)
        return l.load_item()
