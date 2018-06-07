# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class BiqugePipeline(object):
    def __init__(self):
        self.mongo_cli = pymongo.MongoClient(host='x.x.x.x', port=xxxxx)

    def process_item(self, item, spider):
        db = self.mongo_cli.bqg
        if item['book_cl'] == '玄幻小说':
            col = db.xuanhuan
        elif item['book_cl'] == '修真小说':
            col = db.xiuzhen
        elif item['book_cl'] == '都市小说':
            col = db.dushi
        elif item['book_cl'] == '历史小说':
            col = db.lishi
        elif item['book_cl'] == '网游小说':
            col = db.wangyou
        elif item['book_cl'] == '科幻小说':
            col = db.kehuan
        elif item['book_cl'] == '恐怖小说':
            col = db.kongbu
        elif item['book_cl'] == '全本小说':
            col = db.quanben
        else:
            col = db.other
        col.insert(dict(item))
