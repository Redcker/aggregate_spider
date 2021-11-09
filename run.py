#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 22:32
# @File    : run.py
# @Software: PyCharm


from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess


def main():
    """
    启动所有爬虫
    :return:
    """
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    didntWorkSpider = []

    for spider_name in process.spiders.list():
        if spider_name in didntWorkSpider:
            continue
        print("Running spider %s" % (spider_name))
        process.crawl(spider_name)
    process.start()


if __name__ == '__main__':
    import time

    s = time.time()
    main()
    print(time.time() - s)
