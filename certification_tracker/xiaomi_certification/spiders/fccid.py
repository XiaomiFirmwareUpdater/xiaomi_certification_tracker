# -*- coding: utf-8 -*-
from scrapy import Spider


class FccidSpider(Spider):
    name = 'fccid'
    allowed_domains = ['fccid.io']
    start_urls = ['https://fccid.io/2AFZZ/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.fccid_pipeline.FccidPipeline': 400
        }
    }

    def parse(self, response):
        table = response.xpath('//table[@class="table"]')[1]
        items = table.xpath('.//td[position() mod 2 = 1]')
        for item in items:
            yield {
                'model': item.xpath('.//a/text()').get(),
                'date': item.xpath('.//br/following::text()').get(),
                'certification': item.xpath('.//a/@href').get()
            }
