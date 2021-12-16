import time

import scrapy

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ..items import PartnersDirectoryItem
from scrapy.loader import ItemLoader


class PartnerDirSpider(scrapy.Spider):
    name = 'partner_dir'
    allowed_domains = ['fairtradecertified.org']
    start_urls = ['https://partner.fairtradecertified.org/directory/results']

    def start_requests(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse,
            wait_time=30,
            wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '.search-results'))
        )

    def parse(self, response):
        # Driver object selected from response meta data
        driver = response.meta['driver']

        companies_len = driver.find_elements(By.CLASS_NAME, 'profile')
        print('COMPANIES LENGTH: ', len(companies_len))

        # if len(companies_len) == 25:
        #     # Select drop down menu & click 100 results per page
        #     drop_down_menu = driver.find_element(By.CSS_SELECTOR, '.page-size-container')
        #     drop_down_menu.find_element(By.CSS_SELECTOR, 'a').click()
        #     drop_down_menu.find_element(By.CSS_SELECTOR, 'ul li:last-child').click()
        #
        #     WebDriverWait(driver, 60).until(
        #         EC.presence_of_element_located(
        #             (By.CSS_SELECTOR, '.profile:nth-child(26)')
        #         )
        #     )

        # companies_len = driver.find_elements(By.CLASS_NAME, 'profile')

        # Converting selenium page source to scrapy selector
        sel = scrapy.selector.Selector(text=driver.page_source)

        # Grabbing all the profiles
        profiles = sel.css('.profile')
        print('PROFILES LENGTH: ', len(profiles))

        for profile in profiles:
            title = profile.css('.display-name::text').get().strip()
            country = profile.css('.country > span::text').get()
            category = profile.css('.record-type span::text').get()
            marketing_cat = profile.css('.marketing-categories > span::text').get()
            FTUSA_id = profile.css('.certs-info div:nth-child(1)::text').get()
            FLO_id = profile.css('.certs-info div:nth-child(2)::text').get()

            country = self._strip_str(country)
            category = self._strip_str(category)
            marketing_cat = self._strip_str(marketing_cat)
            FTUSA_id = self._strip_str(FTUSA_id)
            FLO_id = self._strip_str(FLO_id)

            # print('PROFILE: ', title, country.upper(), category, marketing_cat, FTUSA_id, FLO_id)

            profile_url = profile.css('.view-profile::attr(href)').get()
            if profile_url:
                profile_url = f'https://partner.fairtradecertified.org{profile_url}'
                print('URL: ', profile_url)

                yield SeleniumRequest(
                    url=profile_url,
                    callback=self.parse_profile,
                    meta={
                        'title': title,
                        'country': country,
                        'category': category,
                        'marketing_cat': marketing_cat,
                        'FTUSA_id': FTUSA_id,
                        'FLO_id': FLO_id,
                    }
                )
            else:
                l = ItemLoader(
                    item=PartnersDirectoryItem(),
                    selector=response
                )

                l.add_value('title', title)
                l.add_value('country', country)
                l.add_value('category', category)
                l.add_value('marketing_cat', marketing_cat)
                l.add_value('FTUSA_id', FTUSA_id)
                l.add_value('FLO_id', FLO_id)

                yield l.load_item()

        # titles = sel.css('.display-name::text').getall()
        # titles = [title.strip() for title in titles]
        #
        # print(len(titles))
        # print(titles)

        time.sleep(5)

    def parse_profile(self, response):
        # print(response.meta)
        l = ItemLoader(
            item=PartnersDirectoryItem(),
            selector=response
        )

        title = response.meta['title']
        country = response.meta['country']
        category = response.meta['category']
        marketing_cat = response.meta['marketing_cat']
        FTUSA_id = response.meta['FTUSA_id']
        FLO_id = response.meta['FLO_id']

        l.add_value('title', title)
        l.add_value('country', country)
        l.add_value('category', category)
        l.add_value('marketing_cat', marketing_cat)
        l.add_value('FTUSA_id', FTUSA_id)
        l.add_value('FLO_id', FLO_id)

        yield l.load_item()


    @staticmethod
    def _strip_str(str_data: str):
        return str_data.strip().lower() if str_data is not None else ''
