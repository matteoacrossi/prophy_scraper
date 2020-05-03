# -*- coding: utf-8 -*-
from scrapy import Item, Field

class ArticleItem(Item):
    title = Field()
    publish_date = Field()
    authors = Field()
    citations = Field()
    citing_articles = Field()
    paperId = Field()
    arXivId = Field()
    doi = Field()
    year = Field()

class LinkItem(Item):
    source = Field()
    target = Field()