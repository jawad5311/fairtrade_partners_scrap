# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PartnersDirectoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    country = scrapy.Field()
    category = scrapy.Field()
    marketing_cat = scrapy.Field()
    FTUSA_id = scrapy.Field()
    FLO_id = scrapy.Field()
    website = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
