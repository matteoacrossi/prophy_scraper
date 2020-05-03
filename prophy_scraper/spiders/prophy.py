# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from prophy_scraper.items import ArticleItem, LinkItem
import json

class ProphySpider(CrawlSpider):
    name = 'prophy'
    allowed_domains = ['prophy.science']
    base_url = 'https://prophy.science/api/'
    arxiv_url = 'arxiv/{}'
    article_url = 'articles/{}/full'
    references_url = 'articles/{}/references-to?sort=citations&offset={}'

    def __init__(self, seedfile="my_papers.json", *args, **kwargs):
        super().__init__(*args, **kwargs)
        with open(seedfile, 'r') as file:
            self.my_papers = json.load(file)

    def start_requests(self):
        """ Start the scraping from the provided list of arxiv ids """
        for arxivid in self.my_papers:
            yield scrapy.Request(url=self.base_url + self.arxiv_url.format(arxivid),
                                callback=self.parse_arxiv)

    def parse_arxiv(self, response):
        """ Get Prophy ID from arxiv_id and then scrape it """
        arxivitem = json.loads(response.body)
        paperid = arxivitem['paperId']

        # Scrape the corresponding dataset
        yield scrapy.Request(url=self.base_url + self.article_url.format(paperid),
                             callback=self.parse)


    def parse(self, response):
        """ Parse the response from a call to the /articles/ARTICLEID/full
        endpoint """

        item = ArticleItem()
        json_res = json.loads(response.body)
        item['paperId'] = str(json_res['article']['id'])
        item['title'] = json_res['article']['title']

        # Get arXiv id and DOI
        for origin in json_res['article']['origins']:
            if origin['code'] == 'arxiv':
                item['arXivId'] = origin['originId']
            elif origin['code'] == 'doi':
                item['doi'] = origin['originId']

        item['citations'] = json_res['article']['citationsCount']
        item['year'] = json_res['article']['year']
        yield item

        # Scrape the list of citing articles. They are grouped in pages of 10
        for offset in range(0, item['citations'] + 10, 10):
            yield scrapy.Request(url=self.base_url +
                                 self.references_url.format(item['paperId'], offset),
                                 callback=self.parse_references_to,
                                 cb_kwargs={'paperid': item['paperId']}) # 'offset': 0,}

    def parse_references_to(self, response, paperid):
        """ Parse the endpoint articles/{}/references-to, yielding a link item
        and scraping the article info for each reference """

        json_res = json.loads(response.body)

        references = json_res['referencesTo']
        if not references['hasMoreReferences']:
            self.log('{} has no more references'.format(paperid))

        # Scrape the information for the citing article
        for reference in references['references']:
            yield scrapy.Request(url=self.base_url +
                                 self.article_url.format(reference['articleId']),
                                 callback=self.parse)

            # Create a link between citing article and source article
            link = LinkItem()
            link['source'] = str(reference['articleId'])
            link['target'] = str(paperid)

            yield link
