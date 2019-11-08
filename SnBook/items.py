# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SnbookItem(scrapy.Item):
    # define the fields for your item here like:
    menu = scrapy.Field()  # 全部书籍分类,如:文学艺术/少儿
    submenu = scrapy.Field()  # 书籍子类,如:文学艺术下的小说
    books_url = scrapy.Field()  # 子类下所有书籍的地址
    next_page_url = scrapy.Field()  # 下一页的全部书籍的地址
    book_url = scrapy.Field()  # 具体书的地址
    book_name = scrapy.Field()  # 书名
    book_price = scrapy.Field()  # 书价格
    book_store = scrapy.Field()  # 商店名称

    pass
