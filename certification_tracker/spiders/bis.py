# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider


class BisSpider(Spider):
    name = 'bis'
    allowed_domains = ['crsbis.in']
    base_url = "https://www.crsbis.in/BIS/Lims_registration.do?hmode=getLimsData&models"
    start_urls = [f'{base_url}=UE9DTw==/', f'{base_url}=UmVkbWk=', f'{base_url}=WGlhb21p']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.bis_pipeline.BisPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//tr[@valign="top"]')
        for item in items:
            brand = item.xpath('.//td[10]/text()').get().strip()
            if ',' in brand:
                brand = brand.split(',')[0]
            models_info = item.xpath('.//td[11]/text()').get().strip()
            if brand.lower() in ['mi', 'poco', 'redmi', 'xiaomi']:
                for model in re.findall(r'(\bM[0-9A-Z-]{3,}\b)', models_info):
                    yield {
                        'brand': brand.capitalize(),
                        'model': model,
                        'category': item.xpath('.//td[6]/text()').get().strip().replace('\n', '/ '),
                        'certification': item.xpath('.//td[2]/text()').get().strip(),
                        'date': datetime.strptime(
                            item.xpath('.//td[3]/text()').get().strip(), '%d-%b-%Y'
                        ).strftime("%Y-%m-%d")
                    }
