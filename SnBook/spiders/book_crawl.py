# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BookCrawlSpider(CrawlSpider):
    name = 'book_crawl'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com']

    rules = (
        Rule(LinkExtractor(allow=r'https://list\.suning\.com/.*\.html$'), callback='parse_item', ),
        Rule(LinkExtractor(allow=r'https://search\.suning\.com/.*keyword=.*([A-z]|[0-9])$'), callback='parse_item', ),

    )

    def parse_item(self, response):
        item = dict()
        item["title"] = response.xpath('//img[@class="search-loading"]/@alt').extract()
        print(item)
