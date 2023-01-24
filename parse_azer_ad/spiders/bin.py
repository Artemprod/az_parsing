import scrapy
from scrapy.http import HtmlResponse
from parse_azer_ad.items import ParseAzerAdItem

class BinSpider(scrapy.Spider):
    name = 'bin'
    allowed_domains = ['bina.az','ru.bina']
    start_urls = ['https://ru.bina.az/kiraye']

    def parse(self, response:HtmlResponse):
        links = response.xpath('//div[contains(@class, "items_list")]//div[contains(@class, "items")]//a[contains(@class, "link")]//@href').getall()
        for link in links:
            link = f'https://bina.az{link}'
            yield response.follow(url=link, callback=self.parse_items)

    def parse_items(self, response:HtmlResponse):
        item = ParseAzerAdItem()
        name = response.xpath('//div[contains(@class,"services-container")]//h1/text()').get()
        item['url'] = response.url
        item['name'] = name
        # item['is_shop'] = is_shop
        # item['is_vip'] = is_vip
        # item['is_premium'] = is_premium
        # item['price'] = price
        # item['currency'] = currency
        # item['phone_number'] = phone_number
        # item['product_info'] = product_info
        # item['discription'] = discription
        # item['similar_ads'] = similar_ads
        print()
