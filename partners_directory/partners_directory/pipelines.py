# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class PartnersDirectoryPipeline:
    def __init__(self):
        self.conn = sqlite3.connect('fairtrade.db')
        self.curr = self.conn.cursor()
        self.create_table()

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

    def store_db(self, item):
        self.curr.execute(
            """
                insert into fairtrade_partners values (?,?,?,?,?,?,?,?,?)
            """,(
                item['title'][0],
                item['country'][0],
                item['account_cat'][0],
                item['marketing_cat'][0],
                item['ftusa_id'][0],
                item['flo_id'][0],
                item.get('website')[0],
                item.get('phone')[0],
                item.get('email')[0],
            )
        )
        self.conn.commit()

    def process_item(self, item, spider):
        self.store_db(item)
        return item
