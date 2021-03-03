# -*- coding: utf-8 -*-
from scrapy.spiders import CSVFeedSpider


class GooglePlaySpider(CSVFeedSpider):
    name = 'google_play'
    allowed_domains = ['storage.googleapis.com']
    start_urls = ['http://storage.googleapis.com/play_public/supported_devices.csv']
    headers = ['Retail Branding', 'Marketing Name', 'Device', 'Model']
    delimiter = ','

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.google_play_pipeline.GooglePlayPipeline': 400
        }
    }

    def parse_row(self, response, row):
        i = {}
        brand = row['Retail Branding'].lower()
        if brand in ['xiaomi', 'redmi', 'poco']:
            i['name'] = row['Marketing Name']
            i['codename'] = row['Device']
            i['model'] = row['Model']
            return i
