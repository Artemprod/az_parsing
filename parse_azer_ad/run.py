from scrapy import crawler
from scrapy.crawler import CrawlerProcess
from parse_azer_ad import settings
from scrapy.settings import Settings
from parse_azer_ad.spiders.lalafo import LalafoSpider
from parse_azer_ad.spiders.bin import BinSpider
from parse_azer_ad.spiders.emlak import EmlakSpider
from parse_azer_ad.spiders.kub import KubSpider
from parse_azer_ad.spiders.tap import TapSpider

from urllib.parse import quote



if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)

    # search_input = str(input("Что будем парсить?: "))
    # search = quote(search_input, encoding='UTF-8')
    search = 'Iphone 13'
    print(search)
    process.crawl(LalafoSpider,search=search)
    # process.crawl(BinSpider)
    # process.crawl(EmlakSpider)
    # process.crawl(KubSpider)

    # process.crawl(TapSpider,search=search)

    process.start()