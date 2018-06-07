# -*- coding: utf-8 -*-
from time import sleep

import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractor import LinkExtractor

from biquge.items import BiqugeItem


class BispiderSpider(CrawlSpider):
    name = 'bispider'
    allowed_domains = ['www.biquge.com.tw']
    start_urls = ['http://www.biquge.com.tw/']
    rules = (
        Rule(LinkExtractor(allow=(r'http://www.biquge.com.tw/[a-z]+/$'))),
        Rule(LinkExtractor(allow=(r'http://www.biquge.com.tw/\d+_\d+/$')), ),
        Rule(LinkExtractor(allow=(r'http://www.biquge.com.tw/\d+_\d+/\d+.html$')), callback='get_content'),
    )

    def get_content(self, response):
        item = BiqugeItem()
        resp_url = response.url
        item['url'] = resp_url
        item['book_id'] = resp_url.split('/')[3]
        item['zhang_id'] = resp_url.split('/')[4].split('.')[0]
        item['book_name'] = response.xpath('//div[@class="bookname"]/div/a[3]/text()').extract_first()
        item['book_cl'] = response.xpath('//div[@class="con_top"]/text()[3]').extract_first()[3:7]
        item['title'] = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        contents = response.xpath('//*[@id="content"]/text()')
        s = ''
        for content in contents:
            if len(content.re('\S+')) > 0:
                s += content.re('\S+')[0]
        item['content'] = s
        return item
    # def parse(self, response):
    #     book_cl = response.xpath('//div[@class="nav"]/ul//li[position()>1]/a/@href').re('/[a-z]+/')
    #     for books_url in book_cl:
    #         # print(books_url)
    #         new_url = response.urljoin(books_url)
    #         print(new_url)
    #         yield scrapy.Request(url=new_url, callback=self.get_book_list)
    #
    #
    #
    #
    # def get_book_list(self, response):
    #     books_list = response.xpath('//div[@id="newscontent"]/div/ul//li/span[1]/a/@href')
    #     # print(len(books_list))
    #     for con_url in books_list:
    #         print(con_url)
    #
    # def zhang_list(self, response):
    #     all_list = response.xpath('//*[@id="list"]/dl//dd/a/@href')
    #     print(response.url)
    #     for url in all_list:
    #         print(url)
