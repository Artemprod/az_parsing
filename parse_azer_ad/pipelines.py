# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import scrapy
from datetime import datetime

class ParseAzerAdPipeline:

    def __init__(self):
        self.client = MongoClient('localhost:27017')
        self.db = self.client['az_parse']


    def process_item(self, item, spider:scrapy.Spider):
        item['created_date'] = self.transform_data(item['created_date'])
        item['discription'] = item['discription'].strip()
        item['name'] = item['name'].strip()
        self.db[spider.name].insert_one(item)
        print()
        return item

    def transform_data(self, data):
        date = datetime.fromtimestamp(data).strftime('%d-%m-%Y %H:%M')
        return date

    def close_sider(self, spider):
        self.client.close()
        
