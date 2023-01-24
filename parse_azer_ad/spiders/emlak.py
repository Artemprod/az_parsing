import scrapy


class EmlakSpider(scrapy.Spider):
    name = 'emlak'
    allowed_domains = ['emlak.az']
    start_urls = ['http://emlak.az/']

    def parse(self, response):
        pass
