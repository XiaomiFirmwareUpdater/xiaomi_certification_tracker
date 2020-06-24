# -*- coding: utf-8 -*-
from scrapy import Spider


class TenaaShoujiSpider(Spider):
    name = 'tenaa_shouji'
    allowed_domains = ['shouji.tenaa.com.cn']
    start_urls = ['http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFGdKI3DQ/ot0g==',
                  'http://shouji.tenaa.com.cn/Mobile/mobileindex_MHSS.aspx?code=ppRNoBcXhFHQLiUSN5abWg==']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.tenaa_shouji_pipeline.TenaaShoujiPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//table[@class="lineGrayTD"]')
        for item in items:
            yield {
                'model': item.xpath('.//tr[2]/td/a/text()').get(),
                'certification': response.urljoin(item.xpath('.//tr[2]/td/a/@href').get()),
                'photo': response.urljoin(item.xpath('.//tr[1]/td[1]/a/img/@src').get())

            }
