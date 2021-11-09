#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/11/5 23:55
# @File    : pipeline_utils.py
# @Software: PyCharm
import time


def clean_line_feed(field):
    """
    清除换行
    :param field: item字段
    :return: 清除后的结果
    """
    return field.replace('\n', '').replace('\r', '')


def clean_item(item):
    """
    清除字段中前后的空格以及所有的换行
    :return: 清洗后的item
    """
    for k, v in item.items():
        if isinstance(v, str):
            item[k] = clean_line_feed(v).strip()


def handle_items_by_rank_type(items):
    """
    将数据用rank_type分类
    :param items: 数据列表
    :return: 入库数据字典
    """
    _data = {}
    for item in items:
        rank_type = item['rank_type']
        if not _data.get(rank_type):
            _data[rank_type] = []
        item.pop('rank_type')  # 去除rank_type字段
        if item not in _data[rank_type]:
            _data[rank_type].append(item)
    data = {
        'timestamp': int(time.time()),  # 入库时间戳
        'data': _data
    }
    return data
