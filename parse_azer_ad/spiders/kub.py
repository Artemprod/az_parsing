import scrapy


class KubSpider(scrapy.Spider):
    name = 'kub'
    allowed_domains = ['kub.az']
    start_urls = ['http://kub.az/']

    def parse(self, response):
        pass
