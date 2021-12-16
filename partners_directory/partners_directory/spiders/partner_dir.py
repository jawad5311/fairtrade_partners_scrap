import time

import scrapy
import selenium

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
    driver = selenium.webdriver.Chrome('E:\webdriver\chromedriver.exe')

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0])

    def parse(self, response):
        # self.driver.get(self.start_urls[0])
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.search-results')
            )
        )

        companies_len = self.driver.find_elements(By.CLASS_NAME, 'profile')
        print('COMPANIES LENGTH: ', len(companies_len))

        if len(companies_len) == 25:
            # Select drop down menu & click 100 results per page
            dd_menu = self.driver.find_element(By.CSS_SELECTOR, '.page-size-container')
            dd_menu.find_element(By.CSS_SELECTOR, 'a').click()
            dd_menu.find_element(By.CSS_SELECTOR, 'ul li:last-child').click()

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.profile:nth-child(26)')
                )
            )

        # Converting selenium page source to scrapy selector
        sel = scrapy.selector.Selector(text=self.driver.page_source)

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
                l = ItemLoader(item=PartnersDirectoryItem())

                l.add_value('title', title)
                l.add_value('country', country)
                l.add_value('category', category)
                l.add_value('marketing_cat', marketing_cat)
                l.add_value('FTUSA_id', FTUSA_id)
                l.add_value('FLO_id', FLO_id)

                yield l.load_item()

    def parse_profile(self, response):
        l = ItemLoader(item=PartnersDirectoryItem())

        title = response.meta['title']
        country = response.meta['country']
        category = response.meta['category']
        marketing_cat = response.meta['marketing_cat']
        FTUSA_id = response.meta['FTUSA_id']
        FLO_id = response.meta['FLO_id']
        website = response.css('.website a::attr(href)').get()
        phone = response.xpath('//*[@fieldtype="tel"]/div/span//text()').get()
        email = response.xpath('//*[@fieldtype="email"]/div/a//text()').get()

        l.add_value('title', title)
        l.add_value('country', country)
        l.add_value('category', category)
        l.add_value('marketing_cat', marketing_cat)
        l.add_value('FTUSA_id', FTUSA_id)
        l.add_value('FLO_id', FLO_id)
        l.add_value('website', website)
        l.add_value('phone', phone)
        l.add_value('email', email)

        yield l.load_item()

    @staticmethod
    def _strip_str(str_data: str):
        return str_data.strip().lower() if str_data is not None else ''
