# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()  # id号
    title = scrapy.Field()  # 书名
    author = scrapy.Field()  # 作者
    publisher = scrapy.Field()  # 出版社
    translator = scrapy.Field()  # 译者
    pub_time = scrapy.Field()  # 出版年
    pages = scrapy.Field()  # 页数
    price = scrapy.Field()  # 定价
    binding = scrapy.Field()  # 装帧
    series = scrapy.Field()  # 丛书
    isbn = scrapy.Field()  # ISBN
    score = scrapy.Field()  # 评分
    number = scrapy.Field()  # 评论人数

