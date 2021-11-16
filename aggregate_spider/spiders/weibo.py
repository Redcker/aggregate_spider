import scrapy
from aggregate_spider.items import WeiBoItem


class WeiboSpider(scrapy.Spider):
    name = 'weibo'
    allowed_domains = ['weibo.com']
    start_urls = ['https://s.weibo.com/top/summary/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.WeiBoPipeline': 300
        }
    }

    custom_headers = {
        "Referer": "https://s.weibo.com/",
        "Cookie": "SUB=1"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.custom_headers)

    def parse(self, response):
        html_data = response.xpath("//table/tbody/tr")
        # topic_list = []
        for sel in html_data:
            item = WeiBoItem()
            item['rank_type'] = 'weibo_hot_search'
            title = sel.xpath("td[2]/a/text()").get()
            tag = sel.xpath("td[3]/i/text()").get()
            mark = sel.xpath("td[2]/span/text()").get()
            rank = sel.xpath("td[1]/text()").get()
            if rank and '•' not in rank:
                item['rank'] = rank
                item['title'] = title
                if tag:
                    item['tag'] = tag if tag else None
                if mark:
                    item['mark'] = mark
                yield item
