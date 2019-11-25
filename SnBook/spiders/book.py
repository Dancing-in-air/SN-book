# -*- coding: utf-8 -*-
import scrapy
from SnBook.items import SnbookItem
from copy import deepcopy
from selenium import webdriver
from lxml import etree


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['suning.com']
    start_urls = ['https://book.suning.com']

    def start_requests(self):
        # 重构star_requests方法,添加cookies
        cookies = "tradeMA=32; _snvd=1573103014556ZKDu8K46pHy; SN_CITY=10_010_1000000_9017_01_10106_4_0; cityId=9017; districtId=10106; hm_guid=01681949-b0ec-40d2-98a4-b98366891654; _device_session_id=p_5af1172f-f005-4372-88c4-d94f25d79f19; _df_ud=87c3e180-3aea-45dd-878b-b259cdfdd037; smhst=646493062|0070167435a10547672246|0070153938a10820148331|0070170340a107672198|0070151041a173041855|0070091633a10583295404|0070213869a10570782544|0070170340a11097919507|0070418556a10065021930|0070078847a10717510914|0070091633; authId=siBDFE536E42BE78A56FBF048E838E9753; secureToken=90BC857D6872B6FAFBD2C26A0E3A3414; _snmc=1; _snsr=baidu%7Cbrand%7C%7Ctitle%7C%25E8%258B%258F%25E5%25AE%2581%25E6%2598%2593%25E8%25B4%25AD*%3A*; _snma=1%7C156980518612672314%7C1573103008705%7C1573782147138%7C1573782148877%7C153%7C20; _snmp=157378214322542305; _snmb=157378214888420447%7C1573782148896%7C1573782148884%7C1; _snzwt=TH8kT516e6cb9da06kIex53d4"
        cookies = {i.split("=")[0].strip(): i.split("=")[1].strip() for i in cookies.split(";")}
        yield scrapy.Request(self.start_urls[0], callback=self.parse, cookies=cookies)

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
                yield scrapy.Request(item["books_url"], callback=self.parse_books, meta={"item": deepcopy(item)})

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
            yield scrapy.Request(item["book_url"], callback=self.parse_book, meta={"item": deepcopy(item)})

        # # 翻页,使用selenium模块获取下一页地址,但是效率超低
        # # 设置无界面浏览
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--disable-gpu")
        # # 禁止图片和css加载
        # prefs = {"profile.managed_default_content_settings.images": 2, 'permissions.default.stylesheet': 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver.get(response.url)
        # html_elements = etree.HTML(driver.page_source)
        # # 获取页面中的下一页部分地址
        # url_part = html_elements.xpath("//a[@id='nextPage']/@href")
        # # 判断是否为最后一页
        # if url_part:
        #     # 获取下一页完整地址
        #     item["next_page_url"] = "https://list.suning.com" + url_part[0]
        #     print(item["next_page_url"])
        #     yield scrapy.Request(item["next_page_url"], callback=self.parse_books, meta={"item": item})

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
