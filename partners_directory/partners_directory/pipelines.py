# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3
import pandas as pd

from scrapy.utils.project import get_project_settings

from quickstart import main
from partners_directory.spiders.partner_dir_api import PartnerDirApiSpider
from partners_directory.items import PartnersDirectoryItem


class PartnersDirectoryPipeline:
    def __init__(self):
        # create connection to the database
        self.conn = sqlite3.connect('fairtrade.db')
        self.curr = self.conn.cursor()  # creates cursor for query executions
        self.create_table()  # Creates table in database

        # Creates connection to Google Sheet API
        # self.service = main()
        columns = PartnersDirectoryItem().fields.keys()  #
        self.df = pd.DataFrame([], columns=columns)

    """
    The following code is used to store data in Google Sheets
    """

    def create_spreadsheet(self):
        """Creates Google Sheet using project and spider name"""

        project_name = get_project_settings().get('BOT_NAME')
        spider_name = PartnerDirApiSpider.name

        sheet_body = {
            'properties': {
                'title': project_name,
                'locale': 'en_US',
                'timeZone': 'Etc/GMT',
                'autoRecalc': 'HOUR'
            },
            'sheets': [{'properties': {'title': spider_name}}]
        }

        self.service.spreadsheets().create(
            body=sheet_body
        ).execute()

    def append_data_to_df(self, item):
        self.df = self.df.append({
            'account_cat': item.get('account_cat'),
            'country': item.get('country'),
            'email': item.get('email'),
            'flo_id': item.get('flo_id'),
            'ftusa_id': item.get('ftusa_id'),
            'marketing_cat': item.get('marketing_cat'),
            'phone': item.get('phone'),
            'title': item.get('title'),
            'website': item.get('website'),
        },
            ignore_index=True)

    def close_spider(self, spider):
        columns = PartnersDirectoryItem().fields.keys()  #
        print(columns)
        print(self.df)
        # self.df.to_csv('close_spider.csv',
        #                index=False)

    """The following code is used to store data in database"""

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
            """, (
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
        self.append_data_to_df(item)
        # self.store_db(item)
        return item
