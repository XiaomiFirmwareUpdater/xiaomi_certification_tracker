# -*- coding: utf-8 -*-
from scrapy import Spider


class MiGlobalSpider(Spider):
    name = 'mi_global'
    allowed_domains = ['mi.com']
    start_urls = ['https://www.mi.com/global/certification/compliance/',
                  'https://www.mi.com/in/certification/compliance/']

    def parse(self, response):
        items = response.xpath('//div[@class="item"]/ul/li')
        for item in items:
            yield {
                'device': item.xpath('.//a/text()').get(),
                'certificate': item.xpath('.//a/@href').get()
            }
