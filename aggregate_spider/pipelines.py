# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.utils.project import get_project_settings
import time
from aggregate_spider.utils import pipeline_utils

settings = get_project_settings()
connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])


class AggregateSpiderPipeline:
    def process_item(self, item, spider):
        return item


class ZhiHuPipeline:
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['zhihu']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('id'):
            if not isinstance(item['id'],int):
                item['id'] = item['id'].split('/')[-1]
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)


class QiDianPipeline:
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['qidian']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_end'):
            item['is_end'] = 0 if item['is_end'] == '连载' else 1
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)


class WeReadPipeline:
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['weread']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)


class DouBanPipeline:
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['douban']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_new'):
            item['is_new'] = 1 if item['is_new'] else 0
        if item.get('star'):
            item['star'] = float(item['star'].split('r')[1][0] + '.' + item['star'].split('r')[1][1])
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)


class MaoYanPipeline:
    rank_type = {
        '1': 'internal',
        '2': 'na',
        '6': 'expect',
        '7': 'hot'
    }
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['maoyan']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)


class ZongHengPineline:
    items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['zongheng']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_end'):
            item['is_end'] = 0 if item['is_end'] == '连载' else 1
        if item.get('update_time'): # 将更新时间补充完整
            item['update_time'] = time.strftime('%Y', time.localtime()) + '-' + item['update_time']
        self.items.append((item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
