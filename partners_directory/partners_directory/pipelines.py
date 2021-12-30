# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3
import pygsheets
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

        # Creates an empty df with item fields as column
        columns = PartnersDirectoryItem().fields.keys()  # grabs items fields as list
        self.df = pd.DataFrame([], columns=columns)  # Creates an empty dataframe

    """
    The following code is used to store data in Google Sheets
    """
    def append_data_to_df(self, item):
        """Append each item to the dataframe"""
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

    def add_data_to_gsheet(self):
        """Upload created dataframe to the google sheets"""
        # scrapy project name, to be used as spreadsheet title
        project_name = get_project_settings().get('BOT_NAME')
        # spider name, to be used as worksheet title
        spider_name = PartnerDirApiSpider.name

        # Creates connection to google sheets api
        conn = pygsheets.authorize(client_secret='credentials.json')
        sheet = conn.create(project_name)  # Creates a spreadsheet
        work_sheet = sheet.add_worksheet(spider_name)  # Creates new worksheet
        # Upload dataframe to the selected worksheet
        work_sheet.set_dataframe(
            df=self.df,  # Dataframe to be updated
            start=(1, 1)  # Range from where the data should be start inserted
        )
        print('Google sheet created successfully!')
        sheet.del_worksheet(sheet.sheet1)  # Deletes default worksheet

    def close_spider(self, spider):
        """This method is called automatically when spider finish crawling"""
        self.add_data_to_gsheet()

    """
    The following code is used to store data in database
    """
    def create_table(self):
        """Creates a table in the connected database"""
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
        """Store data to the database"""
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
