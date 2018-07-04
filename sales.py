# -*- coding: utf-8 -*-
import scrapy


class SalesSpider(scrapy.Spider):
    name = 'sales'
    allowed_domains = ['https://norfolk.craigslist.org/d/cars-trucks/search/cta']
    start_urls = ['http://https://norfolk.craigslist.org/d/cars-trucks/search/cta/']

    def parse(self, response):
        pass
