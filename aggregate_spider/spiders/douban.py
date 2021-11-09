import scrapy
from aggregate_spider.items import MovieRankItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/chart','https://movie.douban.com/coming']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.DouBanPipeline': 300
        }
    }
    def parse(self, response):
        if response.url.endswith('chart'):
            new_movies = response.xpath("//div[@class='indent']/div/table")
            for new_movies in new_movies:
                item = MovieRankItem()
                item['rank_type'] = 'new_movies'
                item['name'] = new_movies.xpath("tr/td[1]/a/@title").get()
                item['cover'] = new_movies.xpath("tr/td[1]/a/img/@src").get()
                item['star'] = new_movies.xpath("tr/td[2]/div/div/span[1]/@class").get()
                item['rating_nums'] = new_movies.xpath("tr/td[2]/div/div/span[2]/text()").get()
                item['rating_count'] = new_movies.xpath("tr/td[2]/div/div/span[3]/text()").get()
                item['introduce'] = new_movies.xpath("tr/td[2]/div/p/text()").get()
                item['id'] = new_movies.xpath("tr/td[1]/a/@href").get().split('/')[-2]
                yield item

            for i in ['listCont2', 'listCont1']:
                week_movies = response.xpath(f"//ul[@id='{i}']/li")
                for week_movie in week_movies:
                    item = MovieRankItem()
                    item['rank_type'] = 'week_movies' if i == 'listCont2' else 'na_movies'
                    item['rank'] = week_movie.xpath("div[1]/text()").get()
                    item['name'] = week_movie.xpath("div[2]/a/text()").get()
                    item['id'] = week_movie.xpath("div[2]/a/@href").get().split('/')[-2]
                    if i == 'listCont2':
                        trend_node_class = week_movie.xpath("span/div/@class").get()
                        trend = int(week_movie.xpath("span/div/text()").get())
                        if trend_node_class == 'down':
                            trend = -1 * trend
                        item['trend'] = trend
                    else:
                        item['is_new'] = week_movie.xpath("div[2]/img/@src").get()
                        item['box_num'] = week_movie.xpath("span/text()").get()
                    yield item
        else:
            movies = response.xpath("//table[@class='coming_list']/tbody/tr")
            for movie in movies:
                item = MovieRankItem()
                item['rank_type'] = 'comming_movies'
                item['release_time'] = movie.xpath("td[1]/text()").get()
                item['name'] = movie.xpath("td[2]/a/text()").get()
                item['produce_location'] = movie.xpath("td[4]/text()").get()
                item['introduce'] = movie.xpath("td[3]/text()").get()
                item['expected_count'] = movie.xpath("td[5]/text()").get()
                item['id'] = movie.xpath("td[2]/a/@href").get().split('/')[-2]
                yield item

