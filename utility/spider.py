import scrapy
from scrapy.crawler import CrawlerProcess
from data.crawler.crawler.spiders.hk import HkSpider


def main():
    process = CrawlerProcess()

    process.crawl(HkSpider)
    process.start(
    )  # the script will block here until the crawling is finished
