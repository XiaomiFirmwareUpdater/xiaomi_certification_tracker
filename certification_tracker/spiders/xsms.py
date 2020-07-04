# -*- coding: utf-8 -*-
import re

from scrapy import Spider
from scrapy.http import TextResponse


class XsmsSpider(Spider):
    name = 'xsms'
    allowed_domains = ['xsms.com.ua']
    start_urls = ['http://xsms.com.ua/phone/imei/all/']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.xsms_pipeline.XsmsPipeline': 400
        }
    }

    def parse(self, response: TextResponse):
        devices = response.xpath('//td[@class="p4te70" and @colspan="2"]').get()
        xiaomi = re.search(r'<b><u>Xiaomi</u></b>:<br>(.*;) <br><b><u>XIAORUI</u>', devices).group(1)
        items = re.findall(r',?(.*?)(?:, |; )', xiaomi)
        for item in items:
            yield {
                'model': item.strip()
            }
