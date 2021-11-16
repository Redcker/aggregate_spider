import scrapy
import re
from aggregate_spider.items import PostItem


class YaohuoSpider(scrapy.Spider):
    name = 'yaohuo'
    allowed_domains = ['yaohuo.me']
    start_urls = ['https://yaohuo.me/bbs/book_list.aspx?action=new&page=1','https://yaohuo.me/bbs/book_list.aspx?action=new&page=2']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.YaoHuoPipeline': 300
        }
    }

    def parse(self, response):
        posts = response.xpath("//body/div")
        for post in posts:
            if 'class="line' in post.extract():
                item = PostItem()
                str_post = post.extract()
                id = re.findall('/bbs-(.*).html?', post.xpath("a[1]/@href").get())[0]
                rank = re.findall('<div class="line.">(.*)\.<', str_post)[0]
                title = post.xpath("a[1]/text()").get()
                extras = list(re.findall('<br>(.*)/<a.*?>(.*)</a>回/(.*)阅', str_post)[0])
                extras[1] = extras[1] + '回'
                extras[2] = extras[2] + '阅'
                item['rank_type'] = 'yaohuo_new'
                item['id'] = id
                item['title'] = title
                item['rank'] = rank
                item['extra'] = '/'.join(extras)
                yield item
