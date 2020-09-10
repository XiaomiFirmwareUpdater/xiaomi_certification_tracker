# -*- coding: utf-8 -*-
from scrapy import Spider


class GCFSpider(Spider):
    name = 'gcf'
    allowed_domains = ['globalcertificationforum.org']
    start_urls = [
        'https://www.globalcertificationforum.org/page-types/public_device_listing/ajaxLoadMoreResult/'
        '?itemclass=.result-item&maxrows=100&q=Xiaomi&pageid=2D915FA3-CDB9-41DA-BB4B414A5C86B4AC&'
        'sortby=certificationDate&sortdirection=desc&page=1']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.gcf_pipeline.GCFPipeline': 400
        }
    }

    def parse(self, response):
        items = response.css('.result-item')
        for item in items:
            yield {
                'model': item.css('td:nth-of-type(3) b::text').get(),
                'device': item.css('td:nth-of-type(4) b::text').get(),
                'date': item.css('td:nth-of-type(5)::text').get(),
                'certification': item.css('a::attr(href)').get()
            }
