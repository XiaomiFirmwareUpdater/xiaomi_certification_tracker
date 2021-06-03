# -*- coding: utf-8 -*-
from scrapy import Spider, Request, FormRequest


class ImdaSpider(Spider):
    name = 'imda'
    allowed_domains = ['eservice.imda.gov.sg']
    data = {
        'dispatch': '',
        'strEquipmentCategory': '',
        'strEquipmentType': '',
        'strTradeName': '',
        'strModelName': '',
        'strCompanyName': 'XIAOMI',
        'trows': '190',
        'rcnt': '0',
        'gotopage': '0'
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.imda_pipeline.IdmaPipeline': 400
        }
    }

    def start_requests(self):
        yield Request(url='https://eservice.imda.gov.sg/tls/searchEquipment.action', callback=self.real_request)

    def real_request(self, response):
        yield FormRequest.from_response(
            response,
            url='https://eservice.imda.gov.sg/tls/viewAllListEquipment.action?param=all',
            formdata=self.data,
            callback=self.parse
        )

    def parse(self, response):
        items = response.xpath('//tbody/tr')
        for item in items:
            yield {
                'brand': item.xpath('.//td[3]/text()').get().strip(),
                'model': item.xpath('.//td[4]/text()').get().strip(),
                'description': item.xpath('.//td[2]/text()').get().strip(),
            }
