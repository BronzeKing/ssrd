import scrapy
from scrapy.crawler import CrawlerProcess
from data.crawler.crawler.spiders.hk import HkSpider
from data.crawler.crawler.spiders.hk import update_category
from ssrd.home.models import Category, Product


def main():
    process = CrawlerProcess()

    process.crawl(HkSpider)
    process.start(
    )  # the script will block here until the crawling is finished

def test():
    data = Product.objects.all()
    [update_category(x) for x in data]