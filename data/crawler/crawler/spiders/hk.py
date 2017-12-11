# -*- coding: utf-8 -*-
import scrapy
from io import BytesIO
import requests
from django.core.files import File
from scrapy.http import Request
from scrapy.http import HtmlResponse
import pandas as pd

from ssrd.home.models import Product, Images, Category
from ssrd.users.models import Documents
from data.home import get_category
from utility.tfIdf import TfIdf

category, ok = Category.objects.get_or_create(name='球机')
data = pd.read_excel('/home/linlin/Documents/data.xlsx')[:21]
products = {x.code for x in Product.objects.all()}
config = [
    dict(name=x['产品名称'], code=x['产品编号'], url=x['产品参数链接'])
    for index, x in data.iterrows() if x['产品编号'] not in products
]
[x.update(category=category) for x in config]
categories = [{
    'parent': {
        'name': '前台设备',
        'parent': {
            'name': '智能化视频监控'
        }
    },
    'name': '枪机'
}, {
    'parent': {
        'name': '前台设备',
        'parent': {
            'name': '智能化视频监控'
        }
    },
    'name': '球机'
}, {
    'parent': {
        'name': '前台设备',
        'parent': {
            'name': '智能化视频监控'
        }
    },
    'name': '半球'
}, {
    'parent': {
        'name': '后台设备',
        'parent': {
            'name': '智能化视频监控'
        }
    },
    'name': 'NVR'
}, {
    'parent': {
        'name': '护罩',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '室外护罩'
}, {
    'parent': {
        'name': '护罩',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '室内护罩'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '枪型/筒型/一体型摄像机支架'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '半球型/海螺型摄像机支架'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '其它摄像机支架'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '红外球机支架'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '5寸球机支架'
}, {
    'parent': {
        'name': '支架',
        'parent': {
            'name': '摄像机配件'
        }
    },
    'name': '4寸球机支架'
}]


def update_category(item):
    tf = TfIdf()
    tf.add_document(item['name'], item['name'])
    sims = [(x, tf.similarities(x['name'])) for x in categories]
    score = max([x[1][1] for x in sims])
    category = [x[0] for x in sims if x[1][1] == score]
    if category:
        item['category'] = get_category(category[0])


def request(url):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }
    return requests.get(url, headers=headers)


def download(url):
    response = request(url)
    name = url.split('/')[-1]
    bio = BytesIO(response.content)
    setattr(bio, 'name', name)
    return File(bio)


def onerror(tag):
    return tag.split('src=')[1].strip("'")


# 支架和护罩
zhijia = [
    'http://www.hikvision.com/cn/prlb_277.html'
    'http://www.hikvision.com/cn/prlb_278.html',
    'http://www.hikvision.com/cn/prlb_279.html',
    'http://www.hikvision.com/cn/prlb_280.html',
    'http://www.hikvision.com/cn/prlb_281.html',
    'http://www.hikvision.com/cn/prlb_282.html',
    'http://www.hikvision.com/cn/prlb_283.html',
    'http://www.hikvision.com/cn/prlb_1160.html',
]


class HkSpider(scrapy.Spider):
    name = 'hk'
    allowed_domains = ['www.hikvision.com']
    # start_urls = [x['url'] for x in config]
    start_urls = zhijia
    item = {}

    def start_requests(self):
        for index, url in enumerate(self.start_urls):
            # self.item = dict(config[index])
            yield Request(url, dont_filter=True, callback=self.parseList)

    def parseList(self, response):
        for i in range(10):
            xpath = '//*[@id="zz{}"]/div[2]/div/div[2]/a/@href'.format(i)
            urls = response.xpath(xpath).extract()
            urls = ['http://www.hikvision.com/cn/' + x for x in urls]
            for url in urls:
                yield Request(url, dont_filter=True, callback=self.parse)

    def parse(self, response):
        item = self.item

        Xdescription = '/html/body/div[5]/div[2]/div[2]/div[2]/div[2]/div/text()'
        description = ''.join(
            map(lambda x: x.strip(), response.xpath(Xdescription).extract()))
        item['description'] = description
        item['code'] = item['name'] = description
        update_category(item)
        obj = Product.objects.filter(name=item['code'])
        if obj:
            return
        Xbackgroup = '//*[@id="middlepic"]/@onerror'
        backgroup = onerror(response.xpath(Xbackgroup).extract_first())
        item['background'] = download(backgroup)
        pictures = [
            '//*[@id="tt1"]/img/@onerror',
            '//*[@id="tt2"]/img/@onerror',
            '//*[@id="tt3"]/img/@onerror',
            '//*[@id="tt4"]/img/@onerror',
            '//*[@id="tt5"]/img/@onerror',
            '//*[@id="tt6"]/img/@onerror',
        ]
        pictures = [response.xpath(x).extract_first() for x in pictures]
        pictures = [onerror(x) for x in pictures if x]
        pictures = [
            Images.objects.create(image=x) for x in map(download, pictures)
        ]

        content = [{'产品概述': ''}, {'详细参数': ''}, {'资料下载': ''}]
        content[0]['产品概述'] = response.xpath(
            '//*[@id="message"]/div').extract_first()
        content[1]['详细参数'] = ''

        xpath = '//*[@id="xz"]/li/a/@href'
        files = map(download, response.xpath(xpath).extract())
        files = Documents.bulk(files)
        _tpl = '<li class="clearfix"><span style="display:none"></span><a href="{url}" target="_blank">{name}</a></li>'
        files = ''.join(
            [_tpl.format(name=x.name, url=x.file.url) for x in files])
        files = '<ul class="clearfix">%s</ul>' % files
        content[2]['资料下载'] = files
        item['content'] = content
        obj = Product.objects.filter(name=item['code'])
        if obj:
            obj = obj[0]
            [setattr(obj, k, v) for k, v in item.items()]
            obj.save()
            obj.pictures.clear()
        obj = Product.objects.create(**item)
        obj.pictures.add(*pictures)
