# -*- coding: utf-8 -*-
from scrapy import Spider


class TenaaCertSpider(Spider):
    name = 'tenaa_cert'
    allowed_domains = ['tenaa.com.cn']
    start_urls = ['http://www.tenaa.com.cn/WSFW/LicenceTop10.aspx?code=B8S953medXcrlUtdCXW6hNpRRSNM6El146e7XzMuOrK'
                  '%2b1bn0UgqVxMIDF8Nvvu2u7d9DHp6wJbbeloURjLgF83KeSorHZbMk5VerrCs2C8W2TxSt%2bnJjW'
                  '%2fLHHgiznjfqI20Qi2oZV22fXl9jV9i1fslZq7xhX%2bXq2X1vV8K456o%3d']

    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.tenaa_cert_pipeline.TennaCertPipeline': 400
        }
    }

    def parse(self, response):
        rows = response.xpath('//table[@id="tblResult"]/tr[position() > 1]')
        for row in rows:
            certification = row.xpath('.//td[2]/a/font/text()').get()
            if certification:
                model = row.xpath('.//td[3]/text()').get()
                date = row.xpath('.//td[6]/text()').get()
                photos = response.urljoin(row.xpath('.//td[9]/a/@href').get())
            else:
                row_number = int(row.xpath('.//td[1]/text()').get())
                certification = rows[row_number - 2].xpath('.//td[2]/a/font/text()').get()
                model = row.xpath('.//td[2]/text()').get()
                date = row.xpath('.//td[5]/text()').get()
                photos = response.urljoin(row.xpath('.//td[8]/a/@href').get())
            yield {
                'certification': certification,
                'model': model,
                'date': date,
                'photos': photos
            }
