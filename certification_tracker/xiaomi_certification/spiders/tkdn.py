# -*- coding: utf-8 -*-
from datetime import datetime

from scrapy import Spider, Request


class TkdnSpider(Spider):
    name = 'tkdn'
    allowed_domains = ['tkdn.kemenperin.go.id']
    base_url = 'http://tkdn.kemenperin.go.id'
    start_urls = ['http://tkdn.kemenperin.go.id/sertifikat_perush.php?id=4eXbKT9nPVUvKv8uQGWZqlxW-yZC7dJ6460WUDT_6So,']

    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.tkdn_pipeline.TkdnPipeline': 400
        }
    }

    def parse(self, response):
        links = response.xpath('//td/a/@href')
        for link in links:
            yield Request(url=f"{self.base_url}/{link.get()})", callback=self.parse_details)

    def parse_details(self, response):
        model = response.xpath('//table/tr[2]/td[3]/text()').get()
        if model.startswith('MI') or model.startswith('Xiaomi'):
            model = model.split(' ')[-1]
            if 'LTE' in model:
                model = response.xpath('//table/tr[3]/td[3]/text()').get()
            yield {
                'model': model,
                'certification': response.xpath('//div[2]/div[2]/b/text()').get(),
                'reference': response.xpath('//div[6]/div[2]/b/text()').get(),
                'date': self.convert_date(response.xpath('//div[3]/div[2]/b/text()').get()),
                'link': response.url
            }

    @staticmethod
    def convert_date(indonesian_date):
        indonesian_date = indonesian_date.split(' ')
        indonesian_months = ['Januari', 'Pebruari', 'Maret', 'April',
                             'Mei', 'Juni', 'Juli', 'Agustus', 'September',
                             'Oktober', 'Nopember', 'Desember']
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        english_month = [i for idx, i in enumerate(months) if indonesian_date[1] == indonesian_months[idx]][0]
        return datetime.strptime(f"{indonesian_date[0]} {english_month} {indonesian_date[2]}", "%d %B %Y"
                                 ).strftime("%Y-%m-%d")
