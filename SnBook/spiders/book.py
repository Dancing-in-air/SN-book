# -*- coding: utf-8 -*-
import scrapy
from SnBook.items import SnbookItem
from copy import deepcopy
import re


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com']

    def parse(self, response):
        menu_list = response.xpath("//div[@class='menu-list']/div[@class='menu-item']")
        for menu in menu_list:
            item = SnbookItem()
            item["menu"] = menu.xpath(".//h3/a/text()").extract_first()  # 获取书籍分类如:文学艺术/少儿
            dd_list = menu.xpath(".//dl/dd/a")
            for dd in dd_list:
                item["submenu"] = dd.xpath("./text()").extract_first()  # 书籍子类,如:文学艺术下的小说
                item["books_url"] = dd.xpath("./@href").extract_first()  # 子类下所有书籍的地址
                if item["books_url"] is None:
                    item["books_url"] = dd.xpath(".//dt[@class='dTitle']/h3/a/@href").extract_first()
                yield scrapy.Request(item["books_url"], callback=self.parse_books, meta={"item": deepcopy(item)},
                                     dont_filter=False)

    def parse_books(self, response):
        """
        获取书籍页面下的所有书籍的url地址
        :param response:
        :return:
        """
        item = response.meta["item"]
        li_list = response.xpath("//ul[@class='clearfix']/li")
        for li in li_list:
            item["book_url"] = "https:" + li.xpath(".//a/@href").extract_first()  # 获取具体书的地址
            yield scrapy.Request(item["book_url"], callback=self.parse_book, meta={"item": deepcopy(item)},
                                 dont_filter=False)
        # 翻页

    def parse_book(self, response):
        """
        获取书籍的详细信息
        :param response:
        :return:
        """

        item = response.meta["item"]
        item["book_name"] = response.xpath("//p[@class='pro-name']/text()").extract_first()  # 获取书名
        item["book_price"] = response.xpath("//div[@id='mainPrice']//dd/span[@class='mainprice']/text("
                                            ")").extract_first()  # 书价格
        item["book_store"] = response.xpath("//div[@id='fix-store']/h3/@title").extract_first()  # # 商店名称
        yield item
