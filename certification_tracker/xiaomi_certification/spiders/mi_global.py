# -*- coding: utf-8 -*-
import scrapy


class MiGlobalSpider(scrapy.Spider):
    name = 'mi_global'
    allowed_domains = ['https://www.mi.com/global/certification/compliance/']
    start_urls = ['http://https://www.mi.com/global/certification/compliance//']

    def parse(self, response):
        pass
