# -*- coding: utf-8 -*-
import scrapy
# from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from bqb.items import BqbItem


class BqbspiderSpider(CrawlSpider):
    name = 'bqbspider'
    allowed_domains = ['www.doutula.com']
    start_urls = ['http://www.doutula.com/article/list/']
    rules = (
        Rule(LinkExtractor(allow=(r'http://www.doutula.com/article/list/\?page=\d+'))),
        Rule(LinkExtractor(allow=(r'http://www.doutula.com/article/detail/\d+')), callback='get_image_parse'),
    )

    def get_image_parse(self, response):
        item = BqbItem()
        item['title'] = response.xpath('//div[@class="pic-title"]/h1/a/text()').extract_first()
        item['data'] = {}
        pic_list = response.xpath('//div[@class="pic-content"]//div[@class="artile_des"]')
        for pic in pic_list:
            pic_url = pic.xpath('./table/tbody/tr[1]/td/a/img/@src').extract_first()
            pic_name = pic.xpath('./table/tbody/tr[1]/td/a/img/@alt').extract_first()
            item['data'][pic_name] = pic_url
        return item
