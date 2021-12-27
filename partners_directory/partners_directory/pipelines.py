# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class PartnersDirectoryPipeline:
    def __init__(self):
        self.curr = sqlite3.connect('fairtrade.db').cursor()

    def create_table(self):
        self.curr.execute(
            """DROP TABLE IF EXISTS fairtrade_partners"""
        )
        self.curr.execute(
            """
                create table fairtrade_partners(
                    title text,
                    country text,
                    account_cat text,
                    marketing_cat text,
                    ftusa_id text,
                    flo_id text,
                    website text,
                    phone text,
                    email text)
            """
        )

    def process_item(self, item, spider):
        return item
