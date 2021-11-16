import scrapy
from aggregate_spider.items import PostItem
import re


class HostlocSpider(scrapy.Spider):
    name = 'hostloc'
    allowed_domains = ['hostloc.com']
    start_urls = ['https://hostloc.com/misc.php?mod=ranklist&type=thread&view=replies&orderby=today']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.HostLocPipeline': 300
        }
    }

    def parse(self, response):
        posts = response.xpath("//table/tr")
        for post in posts:
            item = PostItem()
            title = post.xpath("th/a/text()").get()
            if title:
                id = re.findall('thread-(.*?).html', post.xpath("th/a/@href").get())[0]
                rank = post.xpath("td[1]/text()").get()
                author = post.xpath("td[3]/cite/a/text()").get()
                comment_count = post.xpath("td[4]/a/text()").get()
                item['rank_type'] = 'hostloc_today_rank'
                item['title'] = title
                item['id'] = id
                item['rank'] = rank
                item['extra'] = author + '/' + comment_count + '评论'
                yield item
