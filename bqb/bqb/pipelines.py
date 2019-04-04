# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests


class BqbPipeline(object):

    def process_item(self, item, spider):
        dir_name = dict(item)['title']
        if not os.path.exists("D:\\images\\" + dir_name):
            os.mkdir("D:\\images\\" + dir_name)
        data = dict(item)['data']
        for pic in data:
            pic_url = data[pic]
            print(pic_url)
            print(pic_url.rfind('/'))
            name = pic_url[pic_url.rfind('/') + 1:]
            filename = "D:\\images\\" + dir_name + "\\" + name

            try:
                with open(filename, 'wb') as f:
                    f.write(requests.get(data[pic]).content)
            except IOError as e:
                print(e)
            print(name, '下载完成！')
