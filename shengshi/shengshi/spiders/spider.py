# -*- coding: utf-8 -*-

import scrapy
from scrapy import Request

from shengshi.utils.mysqlutils import mysql_con


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.stats.gov.cn']
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/'
    sql_base = r"""insert into tb_area(name, fatherid, haschild) VALUES {}"""
    start_urls = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html'

    def start_requests(self):
        yield Request(url=self.start_urls, callback=self.parse_province)

    def parse_province(self, response):
        provinces = response.css('.provincetr>td')
        for province in provinces:
            province_name = province.css('a::text').extract_first(None)
            url = province.css('a::attr(href)').extract_first(None)
            if province_name is None or url is None:
                continue
            province_id = mysql_con.op_insert(sql=self.sql_base.format("('" + province_name + "',0,1);"))
            new_url = self.base_url + url
            print('开始准备下载:{}-----{}'.format(province_name, url))
            yield Request(url=new_url, callback=self.parse_city,
                          meta={'province_id': province_id, 'pro_name': province_name})

    def parse_city(self, response):
        citys = response.css('.citytable .citytr td:nth-child(2)')
        fatherid = response.meta.get('province_id')
        for city in citys:
            city_name = city.css('td a::text').extract_first(None)
            city_url = city.css('td a::attr(href)').extract_first(None)
            if city_name is None or city_url is None:
                continue
            city_id = mysql_con.op_insert(sql=self.sql_base.format("('" + city_name + "'," + str(fatherid) + ",1);"))
            new_url = self.base_url + city_url
            print('开始准备下载:{}-----{}-{}'.format(city_url, response.meta.get('pro_name'), city_name))
            yield Request(url=new_url, callback=self.parse_district, meta={'city_id': city_id,
                                                                           'city_name': city_name,
                                                                           'pro_name': response.meta.get('pro_name')
                                                                           })

    def parse_district(self, response):
        countys = response.css('.countytable .countytr td:nth-child(2)')
        fatherid = response.meta.get('city_id')
        total_values = ''
        for index, county in enumerate(countys):
            temp_sql = "('{}', {}, 0)"
            county_name = county.css('td a::text').extract_first(None)
            if county_name is None:
                continue
            temp_sql = temp_sql.format(county_name, fatherid)
            total_values += temp_sql
            if index < len(countys) - 1:
                total_values += ','
            else:
                total_values += ';'
        mysql_con.op_insert(sql=self.sql_base.format(total_values))
        print(response.meta.get('pro_name'), '----', response.meta.get('city_name'), '---- Success!')

