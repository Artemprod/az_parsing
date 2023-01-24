import json
from datetime import datetime

from parse_azer_ad.items import ParseAzerAdItem
import scrapy
from scrapy.http import HtmlResponse
from urllib.parse import quote
from pprint import pprint
from scrapy.loader import ItemLoader

class LalafoSpider(scrapy.Spider):
    name = 'lalafo'
    allowed_domains = ['lalafo.az']
    url_1 = "https://lalafo.az/api/search/v3/feed/search"
    headers = {
        "cookie": "affinity=1661098687.771.215.622780",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Authorization": "Bearer",
        "Connection": "keep-alive",
        "Cookie": "event_user_hash=f5a030f0-edbb-4929-bba9-d406d4f1997c; _fbp=fb.1.1660748128919.799866534; __gads=ID=672ca2a1e99c4898:T=1660748129:S=ALNI_MZuNHFcPQlaNucYVrru9vftqtER4w; _ga=GA1.2.1832978545.1660748129; __utmc=228867841; __utmz=228867841.1660748149.1.1.utmcsr=(direct)^|utmccn=(direct)^|utmcmd=(none); event_session_id=6a17d6d4b61e58733fdb73e5ed90c9bf; _gat=1; _gat_global=1; __gpi=UID=00000a87cc2abb8f:T=1660748129:RT=1661242323:S=ALNI_MbTf7x1qjUQbPATY2AA02OME7lx-w; __utma=228867841.1832978545.1660748129.1661097620.1661242324.3; __utmt=1; lastAnalyticsEvent=listing:feed:listing:ad:view; __utmb=228867841.2.10.1661242324; device_fingerprint=ae90bd459402f497e5aa0b4e000de49e",
        "Referer": "https://lalafo.az/azerbaijan/q-iphone-13",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "country-id": "13",
        "device": "pc",
        "experiment": "novalue",
        "language": "az_AZ",
        "request-id": "react-client_f1698095-d895-40be-a34b-7a453f0388a0",
        "sec-ch-ua": "^\^Chromium^^;v=^\^104^^, ^\^"
    }


    def __init__(self, search):
        super().__init__()
        self.search = quote(search)
        url = f'https://lalafo.az/azerbaijan/q-{self.search.replace(" ", "-")}'
        self.url_api = f'https://lalafo.az/api/search/v3/feed/search?expand=url&q={self.search}'
        self.start_urls = [url]

    def start_requests(self):
        yield scrapy.Request(url=self.url_api, headers=self.headers, callback=self.parse)

    def parse(self, response: HtmlResponse):
        items = ParseAzerAdItem()
        item_list = (data := response.json())['items']
        for item in item_list:
            items['_id'] = f'{datetime.timestamp(datetime.now())}_{item["created_time"]}'
            items['name'] = item['title']
            items['url'] = f'https://lalafo.az{item["url"]}'
            items['is_vip'] = item['is_vip']
            items['is_premium'] = item['is_premium']

            if 'business' in item['user']:
                items['is_shop'] = item['user']['business']['business']
                items['social_links'] = item['user']['business']['features']['social_links']['model']['social_links']
                phone_data = item['user']['business']['features']['contact_phones']['model']['contacts']
                items['location'] = item['user']['business']['features']['location']['model']['locations']
                items['contact_email'] = item['user']['business']['features']['contact_email']['model']['value']
                items['company_page'] = item['user']['business']['features']['site_link']['model']['url']
                phone_list = list()
                for phone in phone_data:
                    phone_list.append(phone['phone'])
                items['phone_number'] = phone_list
            else:
                items['phone_number'] = item['mobile']
                items['location'] = [item['lat'], item['lng']]
            items['price'] = item['price']
            items['currency'] = item['currency']
            items['discription'] = item['description']
            image_data = item['images']
            image_list = list()
            for image in image_data:
                image_list.append(image['original_url'])
            items['images_url'] = image_list

            items['city'] = item['city']
            items['created_date'] = item['created_time']
            items['username'] = item['user']['username']
            yield items


        print('_________________________________________', response.url)
        if 'next' in data['_links']:
            next_link = data['_links']['next']['href']
            yield response.follow(url=f'https://lalafo.az/api/search{next_link}',
                                  headers=self.headers,
                                  callback=self.parse)





