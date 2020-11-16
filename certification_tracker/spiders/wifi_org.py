# -*- coding: utf-8 -*-
from scrapy import Spider


class WifiOrgSpider(Spider):
    name = 'wifi_org'
    allowed_domains = ['wi-fi.org']
    start_urls = [
        'https://www.wi-fi.org/product-finder-results?sort_by=certified&sort_order=desc&keywords=Xiaomi&items=999']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.wifi_org_pipeline.WifiOrgPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//ul[@id="html_data"]/li')
        for item in items:
            yield {
                'device': item.xpath('.//div[@class="details"]/span[1]/text()').get(),
                'model': item.xpath('.//div[@class="details"]/span[2]/text()').get(),
                'category': item.xpath('.//div[@class="details"]/span[5]/text()').get(),
                'date': item.xpath('.//div[@class="details"]/span[6]/text()').get(),
                'certification': item.xpath('.//a[@class="download-cert"]/@href').get()
            }
