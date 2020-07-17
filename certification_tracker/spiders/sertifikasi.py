# -*- coding: utf-8 -*-
from scrapy import Spider, Request


class SertifikasiSpider(Spider):
    name = 'sertifikasi'
    allowed_domains = ['sertifikasi.postel.go.id']
    start_urls = ['https://sertifikasi.postel.go.id/sertifikat/index?key=cust_name&value=Xiaomi']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.sertifikasi_pipeline.SertifikasiPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//tbody/tr')
        for item in items:
            yield {
                'name': item.xpath('.//td[7]/text()').get().strip(),
                'model': item.xpath('.//td[6]/text()').get().strip(),
                'description': item.xpath('.//td[4]/text()').get().strip(),
                'certification': item.xpath('.//td[1]/text()').get().strip(),
            }
        next_page = response.xpath('//a[child::button[contains(text(), "Next")]]/@href').get()
        if next_page:
            yield Request(url=response.urljoin(next_page), callback=self.parse)
