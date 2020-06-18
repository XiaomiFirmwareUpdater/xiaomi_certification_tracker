# -*- coding: utf-8 -*-
from scrapy import Spider


class MiGlobalSpider(Spider):
    name = 'mi_global'
    allowed_domains = ['mi.com']
    start_urls = ['https://www.mi.com/global/certification/compliance/',
                  'https://www.mi.com/in/certification/compliance/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.mi_global_pipeline.MiGlobalPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//div[@class="item"]/ul/li')
        for item in items:
            yield {
                'device': item.xpath('.//a/text()').get(),
                'certification': item.xpath('.//a/@href').get(),
                'region': 'Global' if 'global' in response.url else 'India'
            }
