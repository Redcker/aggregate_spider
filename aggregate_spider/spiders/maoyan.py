import scrapy
from aggregate_spider.items import MovieRankItem
from aggregate_spider.pipelines import MaoYanPipeline
import time


class MaoYanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']

    start_urls = ['https://www.maoyan.com/board/1', 'https://www.maoyan.com/board/7', 'https://www.maoyan.com/board/6',
                  'https://www.maoyan.com/board/2']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.MaoYanPipeline': 300
        }
    }

    custom_headers = {
        "Cookie": "__mta=151476486.1636122977071.1636126618299.1636129049325.33; uuid_n_v=v1; uuid=BBAE4A703E4511EC89993550E45107B00B5388CF346643BBBB1F42035E4EE932; _lxsdk_cuid=17cf08762cfc8-0855b737044a1-57b1a33-1fa400-17cf08762d0c8; _lxsdk=BBAE4A703E4511EC89993550E45107B00B5388CF346643BBBB1F42035E4EE932; __mta=151476486.1636122977071.1636126417635.1636126422267.27; _csrf=c04beb5bfc9a2f33339615bad72c23d41a12e0d609399fb1a7eb8f0f8ef08ce1; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1636122977,1636122996,1636125878,1636129049; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1636129049; _lxsdk_s=17cf08762d0-727-1f6-87e%7C%7C110"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.custom_headers)

    def parse(self, response):
        movies = response.xpath("//dl[@class='board-wrapper']/dd")
        for movie in movies:
            item = MovieRankItem()
            item['rank_type'] = MaoYanPipeline.rank_type[response.url.split('/')[-1]]
            item['rank'] = movie.xpath("i/text()").get()
            item['name'] = movie.xpath("div/div/div/p[1]/a/text()").get()
            item['introduce'] = movie.xpath("div/div/div/p[2]/text()").get()
            item['release_time'] = movie.xpath("div/div/div/p[3]/text()").get().split('：')[1]
            item['cover'] = movie.xpath("a[1]/img[2]/@data-src").get()
            item['id'] = movie.xpath("a[1]/@href").get().split('/')[-1]
            # item['url'] = movie.xpath("a[1]/@href").get()
            yield item
