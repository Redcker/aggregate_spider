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
import redis
import json
import hashlib

settings = get_project_settings()
connection = pymongo.MongoClient(settings['MONGODB_HOST'], settings['MONGODB_PORT'])
redis_connection = redis.Redis(host='localhost', port=6379, db=0)
import copy


class AggregateSpiderPipeline:
    def process_item(self, item, spider):
        return item


class ZhiHuPipeline:
    items = []
    origin_items = []

    def __init__(self):
        db = connection['composite']
        self.col = db['zhihu']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('id'):
            if not isinstance(item['id'], int):
                item['id'] = item['id'].split('/')[-1]
        else:
            item['id'] = hashlib.md5(item['title'].encode()).hexdigest()
        cache_key = 'zhihu_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30)
            _item = {
                'id': item['id'],
                'title': item['title'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(item)
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            # redis_connection.delete('zhihu')
            redis_connection.set('zhihu', str(_data['data']), ex=60 * 11)  # 将数据存在redis


class QiDianPipeline:
    items = []
    origin_items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['qidian']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_end'):
            item['is_end'] = 0 if item['is_end'] == '连载' else 1
        cache_key = 'qidian_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30 * 3)
            _item = {
                'id': item['id'],
                'name': item['name'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(copy.deepcopy(item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            redis_connection.set('qidian', str(_data['data']), ex=60 * 60 * 2)  # 将数据存在redis


class WeReadPipeline:
    items = []
    origin_items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['weread']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        cache_key = 'weread_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30 * 3)
            _item = {
                'id': item['id'],
                'name': item['name'],
                'author': item['author'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(copy.deepcopy(item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            # redis_connection.delete('weread')
            redis_connection.set('weread', str(_data['data']), ex=60 * 60 * 2)  # 将数据存在redis


class DouBanPipeline:
    items = []
    origin_items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['douban']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_new'):
            item['is_new'] = 1 if item['is_new'] else 0
        if item.get('star'):
            item['star'] = float(item['star'].split('r')[1][0] + '.' + item['star'].split('r')[1][1])
        cache_key = 'douban_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30 * 3)
            _item = {
                'id': item['id'],
                'name': item['name'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(copy.deepcopy(item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            # redis_connection.delete('douban')
            redis_connection.set('douban', str(_data['data']), ex=60 * 60)  # 将数据存在redis


class MaoYanPipeline:
    rank_type = {
        '1': 'internal',
        '2': 'na',
        '6': 'expect',
        '7': 'hot'
    }
    items = []
    origin_items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['maoyan']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        cache_key = 'maoyan_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30 * 3)
            _item = {
                'id': item['id'],
                'name': item['name'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(copy.deepcopy(item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            # redis_connection.delete('maoyan')
            redis_connection.set('maoyan', str(_data['data']), ex=60 * 60)  # 将数据存在redis


class ZongHengPineline:
    items = []
    origin_items = []

    def __init__(self):
        db = connection['entertainment']
        self.col = db['zongheng']

    def process_item(self, item, spider):
        pipeline_utils.clean_item(item)
        if item.get('is_end'):
            item['is_end'] = 0 if item['is_end'] == '连载' else 1
        if item.get('update_time'):  # 将更新时间补充完整
            item['update_time'] = time.strftime('%Y', time.localtime()) + '-' + item['update_time']
        cache_key = 'zongheng_' + str(item['id'])
        if not redis_connection.get(cache_key):
            redis_connection.set(cache_key, 1, ex=60 * 60 * 24 * 30 * 3)
            _item = {
                'id': item['id'],
                'name': item['name'],
                'rank_type': item['rank_type']
            }
            self.items.append((_item))
        self.origin_items.append(copy.deepcopy(item))
        return item

    def close_spider(self, spider):
        if self.items:
            data = pipeline_utils.handle_items_by_rank_type(self.items)
            self.col.insert(data)
        if self.origin_items:
            _data = pipeline_utils.handle_items_by_rank_type(self.origin_items)
            # redis_connection.delete('zongheng')
            redis_connection.set('zongheng', str(_data['data']), ex=60 * 60 * 2)  # 将数据存在redis
