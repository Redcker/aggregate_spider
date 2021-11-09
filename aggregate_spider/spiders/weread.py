import scrapy
from aggregate_spider.items import BookRankItem


class WereadSpider(scrapy.Spider):
    name = 'weread'
    allowed_domains = ['weread.qq.com']
    rank_type_map = (
        'all', 'novel_male', 'novel_female', 'rising', 'novel_male_rising', 'novel_female_rising', 'newbook',
        'newbook_novel_male', 'newbook_novel_female', 'novel_male_series', 'novel_female_series', '1900001',
        '2000001', '100000')
    url_template = 'https://weread.qq.com/web/bookListInCategory/{}?maxIndex=0&rank=1'
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.WeReadPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [self.url_template.format(rank) for rank in self.rank_type_map]

    def parse(self, response):
        books = response.json()['books']
        for book in books:
            item = BookRankItem()
            item['rank_type'] = response.url.split('/')[5].split('?')[0]
            item['rank'] = book['searchIdx']
            item['id'] = book['bookInfo']['bookId']
            item['name'] = book['bookInfo']['title']
            item['author'] = book['bookInfo']['author']
            item['cover'] = book['bookInfo']['cover']
            item['category'] = book['bookInfo']['category']
            item['is_end'] = book['bookInfo']['finished']
            item['introduce'] = book['bookInfo']['intro']
            item['reading_count'] = book['readingCount']
            # item['url'] = book.xpath('div[@class="book-mid-info"]/h4/a/@href').get()
            yield item
        # current_index = books[0]['searchIdx']
        # next_index = books[-1]['searchIdx']
        # if current_index < 50:
        #     yield scrapy.Request(response.url.replace(f'maxIndex={current_index-1}', f'maxIndex={next_index+1}'),
        #                          callback=self.parse)
