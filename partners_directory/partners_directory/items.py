# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import MapCompose, TakeFirst


def _convert_none_to_string(value):
    return value if value is not None else ''

class PartnersDirectoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    country = scrapy.Field(output_processor=TakeFirst())
    account_cat = scrapy.Field(output_processor=TakeFirst())
    marketing_cat = scrapy.Field(output_processor=TakeFirst())
    ftusa_id = scrapy.Field(output_processor=TakeFirst())
    flo_id = scrapy.Field(output_processor=TakeFirst())

    website = scrapy.Field(#input_processor=MapCompose(_convert_none_to_string),
                           output_processor=TakeFirst())
    phone = scrapy.Field(#input_processor=MapCompose(_convert_none_to_string),
                         output_processor=TakeFirst())
    email = scrapy.Field(#input_processor=MapCompose(_convert_none_to_string),
                         output_processor=TakeFirst())
