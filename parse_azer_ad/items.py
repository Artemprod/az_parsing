# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, Compose, TakeFirst




class ParseAzerAdItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    is_shop = scrapy.Field()
    is_vip =scrapy.Field()
    is_premium = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    phone_number = scrapy.Field()
    product_info = scrapy.Field()
    discription = scrapy.Field()
    similar_ads = scrapy.Field()
    images_url = scrapy.Field()
    site_links = scrapy.Field()
    location = scrapy.Field()
    contact_email = scrapy.Field()
    company_page = scrapy.Field()
    social_links = scrapy.Field()
    city = scrapy.Field()
    created_date = scrapy.Field()
    username = scrapy.Field()
