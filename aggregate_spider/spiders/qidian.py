import scrapy
from aggregate_spider.items import BookRankItem



class QiDianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['www.qidian.com']
    start_urls = ['https://www.qidian.com/rank/hotsales/page1/',
                  'https://www.qidian.com/rank/readindex/page1/',
                  'https://www.qidian.com/rank/yuepiao/page1/',
                  'https://www.qidian.com/rank/readindex/page1/', 'https://www.qidian.com/rank/newfans/page1/',
                  'https://www.qidian.com/rank/recom/page1/', 'https://www.qidian.com/rank/collect/page1/',
                  'https://www.qidian.com/rank/vipup/page1/', 'https://www.qidian.com/rank/vipcollect/page1/',
                  'https://www.qidian.com/rank/vipreward/page1/', 'https://www.qidian.com/rank/signnewbook/page1/',
                  'https://www.qidian.com/rank/pubnewbook/page1/', 'https://www.qidian.com/rank/newsign/page1/',
                  'https://www.qidian.com/rank/newauthor/page1/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.QiDianPipeline': 300
        }
    }
    def parse(self, response):
        books = response.xpath("//div[@id='book-img-text']/ul/li")
        for book in books:
            item = BookRankItem()
            item['rank_type'] = response.url.split('/')[4]
            item['rank'] = book.xpath('div[@class="book-img-box"]/span[1]/text()').get()
            item['id'] = book.xpath('div[@class="book-mid-info"]/h4/a/@data-bid').get()
            item['name'] = book.xpath('div[@class="book-mid-info"]/h4/a/text()').get()
            item['author'] = book.xpath(
                'div[@class="book-mid-info"]/p[@class="author"]/a[@class="name"][1]/text()').get()
            # item['cover'] = book.xpath('div[@class="book-img-box"]/a/img/@src').get()
            item['category'] = book.xpath('div[@class="book-mid-info"]/p[@class="author"]/a[2]/text()').get()
            # item['sub_category'] = book.xpath('div[@class="book-mid-info"]/p[@class="author"]/a[3]/text()').get()
            item['is_end'] = book.xpath('div[@class="book-mid-info"]/p[@class="author"]/span/text()').get()
            item['introduce'] = book.xpath('div[@class="book-mid-info"]/p[@class="intro"]/text()').get()
            item['last_chapter'] = book.xpath('div[@class="book-mid-info"]/p[@class="update"]/a/text()').get()
            item['update_time'] = book.xpath('div[@class="book-mid-info"]/p[@class="update"]/span/text()').get()
            # item['url'] = book.xpath('div[@class="book-mid-info"]/h4/a/@href').get()
            yield item
        # current_page = int(response.xpath("//div[@id='page-container']/@data-page").get())
        # max_page = int(response.xpath("//div[@id='page-container']/@data-pagemax").get())
        # if current_page < max_page:
        #     yield scrapy.Request(response.url.replace(f'page{current_page}', f'page{current_page + 1}'),
        #                          callback=self.parse)
