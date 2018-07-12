# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request


class SalesSpider(scrapy.Spider):
    name = 'sales'
    allowed_domains = ['craigslist.org']

    # ?max_price=11000&min_auto_year=2008&max_auto_year=2012&max_auto_miles=130000
    def __init__(self, min_price=None, max_price=None, min_auto_year=None, max_auto_year=None, max_auto_miles=None, **kwargs):
        filter_string = '?'
        if min_price:
            filter_string = filter_string + 'min_price=' + str(min_price).strip() + '&'
        if max_price:
            filter_string = filter_string + 'max_price=' + str(max_price).strip() + '&'
        if min_auto_year:
            filter_string = filter_string + 'min_auto_year=' + str(min_auto_year).strip() + '&'
        if max_auto_year:
            filter_string = filter_string + 'max_auto_year=' + str(max_auto_year).strip() + '&'
        if max_auto_miles:
            filter_string = filter_string + 'max_auto_miles=' + str(max_auto_miles).strip() + '&'
        # if no filters supplied, then make filter string empty
        if filter_string == '?':
            filter_string = ''
        # remove last '&' from string
        else:
            filter_string = filter_string[:-1]
        self.start_urls = ['https://norfolk.craigslist.org/search/cta%s' % filter_string,
                          'https://richmond.craigslist.org/search/cta%s' % filter_string,
                          'https://washingtondc.craigslist.org/search/cta%s' % filter_string,
                          'https://charlottesville.craigslist.org/search/cta%s' % filter_string,
                          'https://winchester.craigslist.org/search/cta%s' % filter_string,
                          'https://baltimore.craigslist.org/search/cta%s' % filter_string,
                          'https://fredericksburg.craigslist.org/search/cta%s' % filter_string]
        super(SalesSpider, self).__init__(**kwargs)
        self.log(self.domain)

    def parse(self, response):
        item = {}
        cars = response.xpath('//p[@class="result-info"]')
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        for car in cars:
            inst = {}
            inst['id'] = car.xpath('a/@data-id').extract_first()
            inst['title'] = car.xpath('a/text()').extract_first()
            inst['price'] = car.xpath('.//span[@class="result-price"]/text()').extract_first()
            inst['location'] = car.xpath('.//span[@class="result-hood"]/text()').extract_first()
            inst['post_time'] = car.xpath('time/@datetime').extract_first()
            inst['url'] = car.xpath('a/@href').extract_first()
            item[inst['id']] = inst
        absolute_url = response.url[0:response.url.find('/search')]
        if relative_next_url:
            yield Request(absolute_url + relative_next_url, meta={'item':item})
        yield item