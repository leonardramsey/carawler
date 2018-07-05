# -*- coding: utf-8 -*-
import scrapy


class SalesSpider(scrapy.Spider):
    name = 'sales'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://norfolk.craigslist.org/search/cta',
                  'https://richmond.craigslist.org/search/cta',
                  'https://washingtondc.craigslist.org/search/cta',
                  'https://charlottesville.craigslist.org/search/cta',
                  'https://winchester.craigslist.org/search/cta',
                  'https://baltimore.craigslist.org/search/cta',
                  'https://fredericksburg.craigslist.org/search/cta']

    def parse(self, response):
        item = {}
        cars = response.xpath('//p[@class="result-info"]')
        for car in cars:
            inst = {}
            inst['id'] = car.xpath('a/@data-id').extract_first()
            inst['title'] = car.xpath('a/text()').extract_first()
            inst['price'] = car.xpath('.//span[@class="result-price"]/text()').extract_first()
            inst['location'] = car.xpath('.//span[@class="result-hood"]/text()').extract_first()
            inst['url'] = car.xpath('a/@href').extract_first()
            item[inst['id']] = inst
        return item