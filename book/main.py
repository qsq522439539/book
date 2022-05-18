# -*- coding:utf-8 -*-
# !/usr/bin/python3
import os

minPage = 100
maxPage = 101
for i in range(minPage, maxPage + 1):
    os.system("scrapy crawl book -a page={} --nolog".format(i))
