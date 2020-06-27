# -*- coding: utf-8 -*-
import re
from datetime import datetime

from scrapy import Spider, Request, FormRequest


class SirimSpider(Spider):
    name = 'sirim'
    allowed_domains = ['ecomm.sirim.my']
    url = 'https://ecomm.sirim.my/SirimEnquiry/search_model.aspx'
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'X-MicrosoftAjax': 'Delta=true',
        'Cache-Control': 'no-cache',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Origin': 'https://ecomm.sirim.my',
        'Connection': 'keep-alive',
        'Referer': url,
    }
    data = {
        "ContentPlaceHolder1_TSM1_HiddenField": "",
        "__EVENTARGUMENT": "",
        "ctl00$userid": "",
        "ctl00$screenname": "",
        "ctl00$ContentPlaceHolder1$txtSearch1": "",
        "ctl00$ContentPlaceHolder1$txtSearch2": "Xiaomi",
        "__ASYNCPOST": "true",
    }

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.sirim_pipeline.SirimPipeline': 400
        }
    }

    def start_requests(self):
        yield Request(url=self.url, headers=self.headers, callback=self.real_request)

    def real_request(self, response):
        data = self.data.copy()
        data.update({
            "ctl00$ContentPlaceHolder1$TSM1": "ctl00$ContentPlaceHolder1$UpdatePanel2|ctl00$ContentPlaceHolder1$SFfirstpage",
            "__EVENTTARGET": "ctl00$ContentPlaceHolder1$SFfirstpage",
            "__VIEWSTATE": response.xpath('//input[@id="__VIEWSTATE"]/@value').get(),
            "__VIEWSTATEGENERATOR": response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').get(),
            "ctl00$ContentPlaceHolder1$btnSubmit": "Search"
        })
        yield FormRequest(
            headers=self.headers, url=self.url, formdata=data, callback=self.parse
        )

    def parse(self, response):
        items = response.xpath(
            '//table[@id="ContentPlaceHolder1_gvResults"]/tr[@class="gvrow" or @class="lightgrey"]')
        for item in items:
            details = item.xpath('.//span[contains(@id, "ContentPlaceHolder1_gvResults_lblModel")]/text()').get()
            yield {
                'model': details.split('[')[0].strip(),
                'description': '[' + ''.join(details.split('[')[1:]),
                'certification': item.xpath(
                    './/span[contains(@id, "ContentPlaceHolder1_gvResults_lblTAC")]/text()').get(),
                'category': item.xpath(
                    './/span[contains(@id, "ContentPlaceHolder1_gvResults_lblDevice_Category")]/text()').get(),
                'date': datetime.strptime(
                    item.xpath(
                        './/span[contains(@id, "ContentPlaceHolder1_gvResults_lblApproveDate")]/text()').get(),
                    '%d-%b-%Y').strftime("%Y-%m-%d")
            }

        next_page = response.xpath('//a[@id="ContentPlaceHolder1_SFnextpage"]/@href').get()
        if next_page:
            data = self.data.copy()
            data.update({
                "ctl00$ContentPlaceHolder1$TSM1":
                    "ctl00$ContentPlaceHolder1$UpdatePanel2|ctl00$ContentPlaceHolder1$SFnextpage",
                "ctl00$ContentPlaceHolder1$SFcurrentpage": response.xpath(
                    '//input[@name="ctl00$ContentPlaceHolder1$SFcurrentpage"]/@value').get(),
                "__EVENTTARGET": "ctl00$ContentPlaceHolder1$SFnextpage",
                "__VIEWSTATE": re.search(r'__VIEWSTATE\|([^|]+)', response.text).group(1),
                "__VIEWSTATEGENERATOR": re.search(r'__VIEWSTATEGENERATOR\|([^|]+)', response.text).group(1),
                "__LASTFOCUS": "",
                '': ''
            })
            yield FormRequest(
                headers=self.headers, url=self.url, formdata=data, callback=self.parse, dont_filter=True
            )
