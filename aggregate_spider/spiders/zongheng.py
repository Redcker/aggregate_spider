import scrapy
from aggregate_spider.items import BookRankItem
import re


class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['zongheng.com']
    url_template = 'http://www.zongheng.com/rank/details.html?rt={}&d=1'
    rank_type_map = {'1': 'ticket', '3': '24sale', '4': 'new', '5': 'click', '6': 'recommend', '7': 'welcome',
                     '8': 'finish', '9': 'subscribe', '10': '24update'}

    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.ZongHengPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [self.url_template.format(rank_id) for rank_id in self.rank_type_map.keys()]

    def parse(self, response):
        books = response.xpath("//div[@class='rankpage_box']/div[@class='rank_d_list borderB_c_dsh clearfix']")
        for book in books:
            item = BookRankItem()
            item['rank_type'] = self.rank_type_map[re.findall('rt=(.*)&', response.url)[0]]
            item['rank'] = book.xpath("div[3]/div[@class='rank_d_b_rank']/div[1]/text()").get()
            item['name'] = book.xpath("@bookname").get()
            item['id'] = book.xpath("@bookid").get()
            item['cover'] = book.xpath("div[1]/a/img/@src").get()
            # item['url'] = book.xpath("div[1]/a/@href").get()
            item['author'] = book.xpath("div/div[@class='rank_d_b_cate']/@title").get()
            item['category'] = book.xpath("div/div[@class='rank_d_b_cate']/a[2]/text()").get()
            item['is_end'] = book.xpath("div/div[@class='rank_d_b_cate']/a[3]/text()").get()
            item['introduce'] = book.xpath("div[2]/div[@class='rank_d_b_info']/text()").get()
            item['last_chapter'] = book.xpath("div[2]/div[@class='rank_d_b_last']/text()").get()
            item['last_chapter'] = book.xpath("div[2]/div[@class='rank_d_b_last']/@title").get()
            item['update_time'] = book.xpath(
                "div[2]/div[@class='rank_d_b_last']/span[@class='rank_d_b_time']/text()").get()
            extra = book.xpath("div[3]/div[@class='rank_d_b_rank']/div[2]/text()").get()
            if extra:
                item['extra'] = extra
            yield item
