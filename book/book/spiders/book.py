# -*- coding:utf-8 -*-
# !/usr/bin/python3

import re
from  scrapy import Selector, Spider, Request
from ..items import bookItem

class huangDiZhiJia(Spider):

    name = 'book'
    start_urls = []
    url = 'https://www.huangdizhijia.com'
    allowed_domains = ['www.huangdizhijia.com']

    def __init__(self,  page=None):
        super(Spider, self).__init__()
        self.page = page
        self.start_urls = ["https://www.huangdizhijia.com/novel-{}.html".format(page)]

    def parse(self, response):
        print("当前页: {}".format(self.start_urls[0]))
        contents = response.xpath('//div[@class="tagCol"]/ul/li')
        title = response.xpath('//*[@id="content"]/h1').extract()[0]
        author = response.xpath('//*[@id="content"]/div/div[1]/span/a').extract()[0]
        title = re.findall(r'<h1>(.*?)</h1>', title)[0]
        author = re.findall(r'>(.*?)<', author)[0]
        for i, content in enumerate(contents):
            href = content.xpath('./a/@href').extract()[0]
            ct = content.xpath('./a').extract()[0]
            ct = re.findall(r'>(.*?)<', ct)[0]
            request = Request(self.url + href, callback=self.getText, cb_kwargs={"order": i+1, 'ct': ct, 'title': title, 'author': author})
            yield request

    def getText(self, response, order, ct, title, author):
        item = bookItem()
        text = response.xpath('//div[@class="tagCol"]/p').extract()[0].replace('<br>', '').replace('<p>', '').replace('</p>', '')
        item['title'] = title + '_' + self.page
        item['author'] = author
        item['text'] = ct + '\n' + text
        item['order'] = order
        yield item
