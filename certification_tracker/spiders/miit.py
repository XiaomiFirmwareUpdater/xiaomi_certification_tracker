# -*- coding: utf-8 -*-
import re

from scrapy import Spider


class MiitSpider(Spider):
    name = 'miit'
    allowed_domains = ['zwfw.miit.gov.cn']
    start_url = "https://zwfw.miit.gov.cn/miit/resultSearch?wd=%E5%B0%8F%E7%B1%B3*&pagenow=1"
    start_urls = [start_url]

    custom_settings = {
        'ITEM_PIPELINES': {
            'certification_tracker.pipelines.miit_pipeline.MiitPipeline': 400
        }
    }

    def parse(self, response):
        items = response.xpath('//dd/a/span')
        for item in items:
            item = item.get()
            certification_type = re.search(r'证书种类：([^；]+)；', item)
            name = re.search(r'设备名称：([^；]+)；', item)
            model = re.search(r'设备型号：([^；]+)；', item)
            certification = re.search(r'(?:许可证编号|核准证编号)：([^；]+)；', item)
            date = re.search(r'发证日期：([^；]+)；', item)
            yield {
                'device': name.group(1) if name else "",
                'model': model.group(1) if model else "",
                'category': "Phone" if certification_type else "Other",
                'date': date.group(1) if date else "",
                'certification': certification.group(1) if certification else ""
            }

        # next_page = response.xpath('//a[@aria-label="Next"]/@onclick').get()
        # if next_page:
        #     request_url = self.start_url.split("pagenow=")[0] + 'pagenow=' + next_page.split("'")[1]
        #     yield response.follow(request_url, callback=self.parse)
