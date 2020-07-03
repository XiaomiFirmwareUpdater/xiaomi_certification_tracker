# -*- coding: utf-8 -*-
from scrapy import Spider, Request
from scrapy.http import TextResponse


class CertipediaSpider(Spider):
    name = 'certipedia'
    allowed_domains = ['certipedia.com']
    start_urls = ['https://www.certipedia.com/search/matching_product_certificates?q=Xiaomi']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.certipedia_pipeline.CertipediaPipeline': 400
        }
    }

    def parse(self, response: TextResponse):
        items = response.css('tbody.search-results tr')
        for item in items:
            yield {
                'models': item.xpath('normalize-space(.//td[5]/text())').get().strip(),
                'certification': item.xpath('.//td[6]/a/text()').get().strip(),
                'link': response.urljoin(item.xpath('.//td[6]/a/@href').get())
            }

        next_page = response.xpath('//a[text()="Next"]/@href').get()
        if next_page:
            yield Request(url=response.urljoin(next_page), callback=self.parse)
