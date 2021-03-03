# -*- coding: utf-8 -*-
import re

from scrapy import Spider


class WidevineRevocationTracker(Spider):
    name = 'wvcrl'
    start_urls = ['https://t.me/s/wvcrl']

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.wvcrl_pipeline.WvcrlPipeline': 400
        }
    }

    def parse(self, response):
        items = response.css('.tgme_widget_message_text *::text').getall()
        items = '\n'.join(items).split('ℹ️')[1:]
        for item in items:
            item = item.strip()
            if "revoked" in item:
                continue
            manufacturer = re.search(r'Manufacturer: \n(.*)', item).group(1)
            if not (manufacturer and manufacturer.lower() in ["xiaomi", "redmi", "poco"]):
                continue
            method = re.search(r'Provisioning method: \n(.*)', item)
            yield {
                "manufacturer": manufacturer,
                "model": re.search(r'Model: \n(.*)', item).group(1),
                "soc": re.search(r'SOC: \n(.*)', item).group(1),
                "type": re.search(r'Device type: \n(.*)', item).group(1),
                "certification": re.search(r'New device: \n(\d+)', item).group(1),
                "date": re.search(r'Model year: \n(\d+)', item).group(1),
                "level": re.search(r'Security level: \n(.*)', item).group(1),
                "method": method.group(1) if method else None
            }
