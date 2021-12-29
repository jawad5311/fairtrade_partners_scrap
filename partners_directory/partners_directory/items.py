# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import TakeFirst


class PartnersDirectoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    account_cat = scrapy.Field(output_processor=TakeFirst())
    marketing_cat = scrapy.Field(output_processor=TakeFirst())
    ftusa_id = scrapy.Field(output_processor=TakeFirst())
    flo_id = scrapy.Field(output_processor=TakeFirst())

    website = scrapy.Field(output_processor=TakeFirst())
    phone = scrapy.Field(output_processor=TakeFirst())
    email = scrapy.Field(output_processor=TakeFirst())
