# -*- coding: utf-8 -*-
import json

from scrapy import Spider, FormRequest


class BluetoothSpider(Spider):
    name = 'bluetooth'
    allowed_domains = ['launchstudio.bluetooth.com']
    request = {"searchString": "Xiaomi", "searchQualificationsAndDesigns": "true", "searchDeclarationOnly": "true",
               "searchEndProductList": "false", "searchPRDProductList": "true", "searchMyCompany": "false",
               "productTypeId": "0", "specName": "0", "bqaApprovalStatusId": "-1", "bqaLockStatusId": "-1",
               "listingDateEarliest": "", "listingDateLatest": "", "userId": "0", "memberId": "null", "layers": "[]",
               "maxResults": "5000"}

    custom_settings = {
        'ITEM_PIPELINES': {
            'xiaomi_certification.pipelines.bluetooth_pipeline.BluetoothPipeline': 400
        }
    }

    def start_requests(self):
        yield FormRequest(
            url='https://launchstudio.bluetooth.com/Listings/Search',
            formdata=self.request,
            callback=self.parse
        )

    def parse(self, response):
        data = json.loads(json.loads(response.body.decode('utf8')))
        for item in data:
            yield {
                'name': item.get('name') or item.get('Name'),
                'certification': f"https://launchstudio.bluetooth.com/ListingDetails/{item.get('ListingId')}",
                'items': item.get('ProductListings'),
                'type': item.get('Spec'),
                'date': item.get('ListingDate').split('T')[0]
            }
