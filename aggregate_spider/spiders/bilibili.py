import re

import scrapy
from aggregate_spider.items import PostItem
import time


def get_week_time():
    start_time = time.mktime(time.strptime('20211111', '%Y%m%d'))
    start = 138
    now = time.time()
    days = ((now - start_time) / 60 / 60 / 24) // 7
    return int(days) + start


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://api.bilibili.com/x/web-interface/popular?ps=50&pn=1',
                  'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all',
                  'https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&page=1',
                  'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'.format(get_week_time())]
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.BiliBiliPipeline': 300
        }
    }

    def parse(self, response):
        posts = response.json()['data']['list']
        for post in posts:
            item = PostItem()
            item['rank_type'] = self.get_rank_type(response.url)
            item['id'] = post['bvid']
            item['title'] = post['title']
            view = post['stat']['view']
            danmu = post['stat']['danmaku']
            item['cover'] = post['pic']
            item['extra'] = str(round(view / 10000, 1)) + '万浏览 ' + str(danmu) + '弹幕'
            yield item

    def get_rank_type(self, url):
        if 'popular?ps' in url:
            return f'{self.name}_popular'
        elif 'all' in url:
            return f'{self.name}_all'
        elif 'precious' in url:
            return f'{self.name}_precious'
        elif 'series/one' in url:
            return f'{self.name}_week'
