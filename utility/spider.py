import re

import requests
from io import BytesIO
# import scrapy
# from scrapy.crawler import CrawlerProcess
# from data.crawler.crawler.spiders.hk import HkSpider
# from data.crawler.crawler.spiders.hk import update_category
from django.core.files import File
from ssrd.home.models import Category, Product, Images


def main():
    process = CrawlerProcess()

    process.crawl(HkSpider)
    process.start(
    )  # the script will block here until the crawling is finished

def test():
    data = Product.objects.all()
    [update_category(x) for x in data]

def picture():
    objs = Product.objects.all()
    ptn = re.compile(r'(/UploadFile/Image/\d+\.png)')
    for obj in objs:
        content = obj.content
        if content and '产品概述' in content[0]:
            txt = obj.content[0]['产品概述']
            pct = ptn.findall(txt)
            if pct:
                pct = pct[0]
                url = 'http://www.hikvision.com/' + pct
                pct = download(url)
                image = Images.objects.create(image=pct)
                txt = ptn.sub(image.image.url, txt)
                obj.content[0]['产品概述'] = txt
                obj.save()

def download(url):
    response = request(url)
    name = url.split('/')[-1]
    bio = BytesIO(response.content)
    setattr(bio, 'name', name)
    return File(bio)


def request(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    return requests.get(url, headers=headers)
