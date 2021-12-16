import time

import scrapy

from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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

        if len(companies_len) == 25:
            # Select drop down menu & click 100 results per page
            drop_down_menu = driver.find_element(By.CSS_SELECTOR, '.page-size-container')
            drop_down_menu.find_element(By.CSS_SELECTOR, 'a').click()
            drop_down_menu.find_element(By.CSS_SELECTOR, 'ul li:last-child').click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.profile:nth-child(26)')
                )
            )

        sel = scrapy.selector.Selector(text=driver.page_source)

        titles = sel.css('.display-name::text').getall()
        titles = [title.strip() for title in titles]

        print(len(titles))
        print(titles)



        time.sleep(5)
