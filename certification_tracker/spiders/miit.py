# -*- coding: utf-8 -*-
import json

from scrapy import Spider, Request


class MiitSpider(Spider):
    name = 'miit'
    allowed_domains = ['ythzxfw.miit.gov.cn']
    url = "https://ythzxfw.miit.gov.cn/user-center/tbAppSearch/selectResult"
    headers = {
        'Authorization': 'null',
        'Content-Type': 'application/json;charset=utf-8',
        'Origin': 'https://ythzxfw.miit.gov.cn',
        'Connection': 'keep-alive',
        'Referer': 'https://ythzxfw.miit.gov.cn/resultQuery',
    }
    data = '{"categoryId": "", "currentPage": 1, "pageSize": 500, "searchContent": "小米"}'

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.miit_pipeline.MiitPipeline': 400
        }
    }

    def start_requests(self):
        yield Request(
            url=self.url,
            method="POST",
            headers=self.headers,
            body=self.data,
            callback=self.parse
        )

    def parse(self, response):
        data = json.loads(response.body.decode('utf8'))
        if not data and not data.get('success') is False:
            return
        data = data['params']['tbAppArticle']['list']
        for item in data:
            certification_type = item.get('articleField08')  # 证书种类
            name = item.get('articleField02')  # 设备名称
            model = item.get('articleField03')  # 设备型号
            certification = item.get('articleField01')  # 许可证编号
            date = item.get('articleField06') or item.get('createTime')  # 发证日期
            yield {
                'device': name if name else "",
                'model': model if model else "",
                'category': "Phone" if certification_type else "Other",
                'date': date.split(' ')[0] if date else "",
                'certification': certification if certification else ""
            }
