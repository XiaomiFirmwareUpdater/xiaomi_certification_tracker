# -*- coding: utf-8 -*-
from scrapy import Spider, Request


class FccidSpider(Spider):
    name = 'fccid'
    allowed_domains = ['fccid.io']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'fccid.io',
    }
    start_urls = ['https://fccid.io/2AFZZ/', 'https://fccid.io/2AIMR/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.fccid_pipeline.FccidPipeline': 400
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, self.parse, headers=self.headers)

    def parse(self, response):
        table = response.xpath('//table[@class="table"]')[1]
        items = table.xpath('.//td[position() mod 2 = 1]')
        for item in items:
            yield {
                'model': item.xpath('.//a/text()').get(),
                'date': item.xpath('.//br/following::text()').get(),
                'certification': item.xpath('.//a/@href').get()
            }
