import scrapy
from scrapy.http import HtmlResponse
from parse_azer_ad.items import ParseAzerAdItem
from urllib.parse import quote



class TapSpider(scrapy.Spider):
    name = 'tap'
    allowed_domains = ['tap.az', 'ru.tap.az']

    def __init__(self, search):
        super().__init__()
        url = f"https://ru.tap.az/elanlar?utf8=%E2%9C%93&order=&q%5Buser_id%" \
              f"5D=&q%5Bcontact_id%5D=&q%5Bprice%5D%5B%5D=&q%5Bprice%5D%5B%5D=&q%5" \
              f"Bregion_id%5D=&q%5Bkeywords%5D={quote(search,encoding='UTF-8')}"
        print(url)
        self.start_urls = [url]
        self.first_part ='https://ru.tap.az'

    def parse(self, response:HtmlResponse):
        links = response.xpath('//div[contains(@class,"products-i")]//a[contains(@target,"_blank")]//@href').getall()
        print()
        for link in links:
            link=self.first_part+link
            yield response.follow(link, callback=self.parse_items)

        next_link = response.xpath('//div[contains(@class,"next")]//@href').get()
        print()
        if next_link:
            next_link = f'https://ru.tap.az{next_link}'
            print()
            yield response.follow(next_link, callback=self.parse)


    def parse_items(self,response:HtmlResponse):
        # глобальные переменные для сохранения данных
        phone_number = dict()
        product_info = dict()
        list_of_properties = list()

        item = ParseAzerAdItem()
        name = response.xpath('//div[contains(@class, "title-container")]//h1/text()').get()
        is_shop = response.xpath('//div[contains(@class, "shop-contact")]').get()

        if is_shop:
            is_shop = True
            phones_numbers = response.xpath('//div[contains(@class, "shop-contact")]//a[contains(@class, "number")]//text()').getall()
            for i in phones_numbers:
                phone_number[f'phone_number {phones_numbers.index(i)+1}'] = i
        else:
            is_shop = False
        is_vip = response.xpath('//a[contains(@id, "set_vipped")]/text()').get()
        if is_vip == 'VIP Объявление':
            is_vip = True
        else:
            is_vip = False

        is_premium = response.xpath('//a[contains(@id, "set_featured")]/text()').get()
        if is_premium == 'Премиум':
            is_premium = True
        else:
            is_premium = False
        price = response.xpath('//div[contains(@class, "middle")]//span[contains(@class, "price-val")]//text()').get()
        currency = response.xpath('//div[contains(@class, "middle")]//span[contains(@class, "price-cur")]//text()').get()
        properties = response.xpath('//table[contains(@class, "properties")]//tr')

        for prop in properties:
            list_of_properties.append(prop.xpath('td//text()').getall())
            for i in list_of_properties:
                product_info[f'{i[0].replace("?","")}'] = i[1]

        discription = response.xpath('//div[contains(@class, "lot-text")]//p//text()').getall()
        discription = ','.join([i.strip() for i in discription])
        similar_ads = response.xpath('//div[contains(@class, "products")]//a[contains(@class, "-link")]//@href').getall()
        similar_ads = [f'ru.tap.az{i}' for i in similar_ads]
        item['url'] = response.url
        item['name'] = name
        item['is_shop'] = is_shop
        item['is_vip'] = is_vip
        item['is_premium'] = is_premium
        item['price'] = price
        item['currency'] = currency
        item['phone_number'] = phone_number
        item['product_info'] = product_info
        item['discription'] = discription
        item['similar_ads'] = similar_ads
        print()
        yield item
