import scrapy
from bs4 import BeautifulSoup
import re
from aggregate_spider.items import ZhiHuItem


class ZhiHuSpider(scrapy.Spider):
    """
    知乎日榜爬虫
    """
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/billboard', 'https://www.zhihu.com/topsearch',
                  'https://www.zhihu.com/appview/content-rank?id=car',
                  'https://www.zhihu.com/appview/content-rank?id=school',
                  'https://www.zhihu.com/appview/content-rank?id=sport',
                  'https://www.zhihu.com/appview/content-rank?id=film',
                  'https://www.zhihu.com/hot/daily']
    custom_settings = {
        'ITEM_PIPELINES': {
            'aggregate_spider.pipelines.ZhiHuPipeline': 300
        }
    }
    custom_headers = {
        "Referer": "https://www.zhihu.com/"
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.custom_headers)

    def parse(self, response):
        if response.url.endswith("billboard"):  # 热榜
            soup = BeautifulSoup(response.text, "lxml")
            script_text = soup.find("script", id="js-initialData").get_text
            rule = '"hotList":(.*?),"guestFeeds"'
            result = re.findall(rule, str(script_text))
            temp = result[0].replace("false", "False").replace("true", "True")
            hot_list = eval(temp)
            for index, hot in enumerate(hot_list):
                topic = hot['target']
                item = ZhiHuItem()
                item['rank_type'] = 'hot_top'
                item['rank'] = index + 1
                item['id'] = topic['link']['url']
                item['title'] = topic['titleArea']['text']
                # item['excerpt'] = topic['titleArea']['text']
                item['extra'] = topic['metricsArea']['text']
                item['cover'] = topic['imageArea']['url']
                # item['url'] = topic['link']['url']
                item['answer_count'] = hot['feedSpecific']['answerCount']
                yield item
        elif response.url.endswith("topsearch"):  # 热搜
            topics = response.xpath("//div[@class='TopSearchMain-list']/div[@class='TopSearchMain-item']")
            for topic in topics:
                item = ZhiHuItem()
                item['rank_type'] = 'hot_search'
                item['rank'] = topic.xpath("div[@class='TopSearchMain-index']/text()").get()
                item['title'] = topic.xpath(
                    "div[@class='TopSearchMain-titleWrapper']/div[@class='TopSearchMain-title']/text()").get()
                yield item
        elif response.url.endswith('daily'):  # 日报
            soup = BeautifulSoup(response.text, "lxml")
            script_text = soup.find("script", id="js-initialData").get_text
            rule = '"totals":10},"data":(.*)},"hotHighlight"'
            result = re.findall(rule, str(script_text))
            temp = result[0].replace("false", "False").replace("true", "True")
            topics = eval(temp)
            for topic in topics:
                target = topic['target']
                item = ZhiHuItem()
                item['rank_type'] = 'daily'
                item['id'] = target['question']['id']
                item['rank'] = topic['index'] + 1
                item['title'] = target['question']['title']
                item['excerpt'] = target['excerpt']
                item['voteup_count'] = target['voteupCount']
                item['comment_count'] = target['commentCount']
                item['extra'] = target['tags'][0]['name']
                yield item
            # topics = response.xpath("//div[@class='css-nch6sp']")
            # for topic in topics:
            #     item = ZhiHuItem()
            #     item['rank_type'] = 'daily'
            #     item['id'] = topic.xpath("div[@class='css-9w5xgm']/span/text()").get()
            #     item['rank'] = topic.xpath("div[@class='css-9w5xgm']/span/text()").get()
            #     item['title'] = topic.xpath("div[@class='css-1le6se0']/h2/text()").get()
            #     item['excerpt'] = topic.xpath("div[@class='css-1le6se0']/div[@class='css-eofc2p']/text()").get()[:80]
            #     item['metrics'] = topic.xpath("div[@class='css-1dih7ri']/div[1]/text()").get()
            #     item['extra'] = topic.xpath("div[@class='css-1le6se0']/div[@class='css-dfraw2']/div/text()").get()
            #     yield item
        else:  # 分类榜单
            topics = response.xpath(
                "//div[@class='ContentRank-body']/div[@class='ZVideoCampaignVideo-videoList']/div[@class='ContentRank-contentCard']")
            for topic in topics:
                item = ZhiHuItem()
                item['rank_type'] = response.url.split('=')[1]
                item['rank'] = topic.xpath("div[1]/text()").get()
                item['id'] = topic.xpath("@href").get()
                item['title'] = topic.xpath("div[2]/div[@class='ContentRank-contentCardTitle']/text()").get()
                item['extra'] = topic.xpath("div[2]/div[@class='ContentRank-contentCardHotDegree']/text()").get()
                item['cover'] = topic.xpath("div[@class='ContentRank-contentCardThumbnail']/img/@src").get()
                yield item
