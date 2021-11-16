# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AggregateSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class PostItem(scrapy.Item):
    rank_type = scrapy.Field()
    id = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    excerpt = scrapy.Field()
    metrics = scrapy.Field()
    cover = scrapy.Field()
    url = scrapy.Field()
    answer_count = scrapy.Field()
    extra = scrapy.Field()
    answer_id = scrapy.Field()
    voteup_count = scrapy.Field()
    comment_count = scrapy.Field()


class BookRankItem(scrapy.Item):
    rank_type = scrapy.Field()
    rank = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    cover = scrapy.Field()
    category = scrapy.Field()
    sub_category = scrapy.Field()
    is_end = scrapy.Field()
    introduce = scrapy.Field()
    last_chapter = scrapy.Field()
    update_time = scrapy.Field()
    url = scrapy.Field()
    reading_count = scrapy.Field()
    extra = scrapy.Field()




class MovieRankItem(scrapy.Item):
    rank_type = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    cover = scrapy.Field()
    star = scrapy.Field()
    rating_nums = scrapy.Field()
    rating_count = scrapy.Field()
    introduce = scrapy.Field()
    rank = scrapy.Field()
    url = scrapy.Field()
    trend = scrapy.Field()
    is_new = scrapy.Field()
    box_num = scrapy.Field()
    release_time = scrapy.Field()
    produce_location = scrapy.Field()
    expected_count = scrapy.Field()

class WeiBoItem(scrapy.Item):
    rank_type = scrapy.Field()
    id = scrapy.Field()
    rank = scrapy.Field()
    title = scrapy.Field()
    tag = scrapy.Field()
    mark = scrapy.Field()

