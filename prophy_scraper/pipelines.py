# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.exporters import JsonItemExporter

from .items import ArticleItem, LinkItem

class ProphyScraperPipeline(object):
    
    def open_spider(self, spider):
        self.file_a = open('articles.json', 'wb')
        self.file_l = open('links.json', 'wb')

        self.exporter_a = JsonItemExporter(self.file_a, encoding='utf-8', ensure_ascii=False)
        self.exporter_a.start_exporting()

        self.exporter_l = JsonItemExporter(self.file_l, encoding='utf-8', ensure_ascii=False)
        self.exporter_l.start_exporting()

    def close_spider(self, spider):

        self.exporter_a.finish_exporting()
        self.exporter_l.finish_exporting()

        self.file_a.close()
        self.file_l.close()

    def process_item(self, item, spider):
        if isinstance(item, ArticleItem):
            self.exporter_a.export_item(item)

        elif isinstance(item, LinkItem):
            self.exporter_l.export_item(item)
        return item