# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class PartnersDirectoryPipeline:
    def __init__(self):
        # create connection to the database
        self.conn = sqlite3.connect('fairtrade.db')
        self.curr = self.conn.cursor()  # creates cursor for query executions
        self.create_table()  # Creates table in database

    def create_table(self):
        # Drops the table if it already exists
        self.curr.execute(
            """DROP TABLE IF EXISTS fairtrade_partners"""
        )
        # Creates a new table in the database
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
        # store scrapped data in the connected database
        self.curr.execute(
            """
                insert into fairtrade_partners values (?,?,?,?,?,?,?,?,?)
            """,(
                item.get('title'),
                item.get('country'),
                item.get('account_cat'),
                item.get('marketing_cat'),
                item.get('ftusa_id'),
                item.get('flo_id'),
                item.get('website'),
                item.get('phone'),
                item.get('email'),
            )
        )
        self.conn.commit()  # commit all the changes to the database

    def process_item(self, item, spider):
        self.store_db(item)
        return item
