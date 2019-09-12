# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import BookItem
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name = 'book'
    allowed_domains = ['book.douban.com']
    # start_urls = ['https://book.douban.com/tag/']
    redis_key = "book"

    def parse(self, response):
        tag_urls = response.xpath("//table[@class='tagCol']//a/@href").getall()
        for tag_url in tag_urls:
            base_page_url = response.urljoin(tag_url)  # 第一页的链接
            for i in range(0, 50):
                url = base_page_url + '?start=%d&type=T' % (i * 20)
                yield scrapy.Request(url, callback=self.parse_book_list)

    def parse_book_list(self, response):
        detail_urls = response.xpath("//a[@class='nbg']/@href").getall()  # 详细页链接
        for detail_url in detail_urls:
            yield scrapy.Request(detail_url, callback=self.parse_book_detail)

    def parse_book_detail(self, response):
        title = response.xpath("//div[@id='wrapper']/h1/span/text()").get()
        infos = response.xpath("//div[@id='info']//text()").getall()
        # print(infos)
        # 1. 先去除所有的冒号
        infos = list(map(lambda info: info.replace(":", ""), infos))  # map(function, iterable, ...) 返回包含每次 function 函数返回值的新列表
        # 2. 再过滤掉所有纯空白字符的
        infos = list(filter(lambda info: re.search(r"\S", info), infos))  # filter(function, iterable) filter() 函数用于过滤序列，过滤掉不符合条件的元素，返回由符合条件元素组成的新列表
        # print("=" * 30)
        # print(infos)
        # print("=" * 30)
        author = publisher = translator = pub_time = pages = price = binding = series = isbn = ""
        for index, info in enumerate(infos):
            if info.strip() == '作者':
                author = re.sub(r'\s', '', infos[index + 1])
            elif info.strip() == '出版社':
                publisher = infos[index + 1]
            elif info.strip() == '译者':
                translator = infos[index + 1]
            elif info.strip() == '出版年':
                pub_time = infos[index + 1]
            elif info.strip() == '页数':
                pages = infos[index + 1]
            elif info.strip() == '定价':
                price = infos[index + 1]
            elif info.strip() == '装帧':
                binding = infos[index + 1]
            elif info.strip() == '丛书':
                series = infos[index + 1]
            elif info.strip() == 'ISBN':
                isbn = infos[index + 1]
        score = response.xpath("//strong[contains(@class,'rating_num')]/text()").get().strip()
        number = response.xpath("//a[@class='rating_people']/span/text()").get()
        book_id = re.search(r'\d+', response.url).group()  # 只找到第一个匹配项
        item = BookItem(id=book_id, title=title, author=author, publisher=publisher, translator=translator,
                        pub_time=pub_time, pages=pages, price=price, binding=binding, series=series, isbn=isbn,
                        score=score, number=number)
        yield item
