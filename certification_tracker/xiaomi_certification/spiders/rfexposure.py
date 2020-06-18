# -*- coding: utf-8 -*-
import re

from scrapy import Spider


class RfexposureSpider(Spider):
    name = 'rfexposure'
    allowed_domains = ['mi.com']
    start_urls = ['https://www.mi.com/global/certification/rfexposure/',
                  'https://www.mi.com/in/certification/rfexposure/']
    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.rfexposure_pipeline.RfExposurePipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//div[@class="item"]/ul/li')
        for item in items:
            device_id = item.xpath('.//p[@class="alink"]/@data-id').get()
            device_info = response.xpath(f'//div[@id="{device_id}"]').get()
            model = re.search(r'model (.*) has', device_info).group(1)
            yield {
                'device': item.xpath('.//p/text()').get(),
                'device_id': device_id,
                'model': model,
                'region': 'Global' if 'global' in response.url else 'India'
            }
