# -*- coding:utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class BilibiliPipeline:
    items = []  #自定义一个列表

    def process_item(self, item, spider):   
        self.items.append(item) #每次spidre给管道传数据时，不直接写入json文件，而是存入列表中。如果直接存入文件，会因为spider异步的原因，导致视频无序。
        return item

    def close_spider(self, spider): #在关闭spider的时候会自动调用此函数
        items_ord = []  
        for i in range(100):    #利用列表中所有字典中的rank值进行排序，最终的结果放在items_ord这个列表中
            for item in self.items:
                if item['rank'] == str(i + 1):
                    items_ord.append(item)
                    break
        with open ("top100.json", "w") as f:    #利用json.dump存入top100.json文件中
            json.dump(items_ord, f, ensure_ascii=False)
