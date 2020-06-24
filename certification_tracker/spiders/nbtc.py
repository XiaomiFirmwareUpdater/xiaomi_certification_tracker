# -*- coding: utf-8 -*-
from scrapy import Spider


class NbtcSpider(Spider):
    name = 'nbtc'
    allowed_domains = ['mocheck.nbtc.go.th']
    start_urls = ['http://mocheck.nbtc.go.th/search?keyword=Xiaomi']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.nbtc_pipeline.NbtcPipeline': 400
        }
    }

    def parse(self, response):
        items = response.css('.item-body.item-block')
        for item in items:
            device = ""
            model = item.css('div.col-xs-12.col-md-2:nth-of-type(2) h4::text').get()
            if ' (' in model:
                device = model.split("(")[1].split(")")[0].strip()
                model = model.split(' ')[0]
            yield {
                'brand': item.css('div.col-xs-12.col-md-2:nth-of-type(1) h4::text').get(),
                'model': model,
                'device': device,
                'certification': item.css('div.col-xs-12.col-md-2:nth-of-type(4) h4::text').get().strip(),
                'link': item.css('div.row > a::attr(href)').get()
            }
