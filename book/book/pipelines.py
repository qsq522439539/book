# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sys
import os
class BookPipeline:

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)

    def close_spider(self, spider):
        self.items.sort(key=lambda i:i['order'])
        cur_path = os.getcwd() + '/书籍/'
        title = self.items[0]['title']
        author = self.items[0]['author']
        file_path = cur_path + title + '_' + author + '.txt'
        if not os.path.exists(cur_path): os.makedirs(cur_path)
        with open(file_path, 'w', encoding='utf-8') as f:
            for i in self.items:
                f.write(i['text'] + '\n')