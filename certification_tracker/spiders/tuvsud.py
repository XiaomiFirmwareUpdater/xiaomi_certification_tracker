# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Spider, Request
from scrapy.http import TextResponse


class TuvsudSpider(Spider):
    name = 'tuvsud'
    allowed_domains = ['certificateexplorer2.tuev-sued.de']
    start_urls = [
        'https://certificateexplorer2.tuev-sued.de/web/ig-tuvs/certificate?lang=en&q=Xiaomi']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.tuvsud_pipeline.TuvsudPipeline': 400
        }
    }

    def parse(self, response: TextResponse):
        items = response.css('div.result')
        item: TextResponse
        for item in items:
            yield {
                'certification': item.css('div.result_title::text').get(),
                'category': item.xpath('.//th/span[contains(text(), "Product")]/following::td/div/text()').get(),
                'models': item.xpath('.//th/span[contains(text(), "Model")]/following::td/div/text()').get().strip(),
                'date': datetime.strptime(
                    item.xpath(
                        './/th/span[contains(text(), "Date")]/following::td/div/text()'
                    ).get().strip(),
                    '%d.%m.%Y').strftime("%Y-%m-%d")

            }
        next_page = response.xpath('//nav/a[1]/@href').get()
        if next_page:
            yield Request(url=response.urljoin(next_page), callback=self.parse)
