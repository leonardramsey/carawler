# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, csv, os
from scrapy.exporters import CsvItemExporter
from openpyxl import Workbook
from scrapy.exceptions import DropItem

# stage 1: read in from interested cars file and car_filter.txt out cars
# if the car title does not have any strings from the filter, remove the result
# if the car's price is outside of the price filter range, remove the car
class CarawlerFilterPipeline(object):

    # open filter files if they exist
    def __init__(self):
        self.car_filter_filename = 'carawler/input/car_filter.txt'
        self.price_filter_filename = 'carawler/input/price_filter.txt'
        try:
            with open(self.car_filter_filename, 'rb') as car_filter:
                self.car_filter = car_filter.readlines()
        except:
            self.cars = None
        try:
            with open(self.price_filter_filename, 'rb') as price_filter:
                self.min_price = int(price_filter.readline())
                self.max_price = int(price_filter.readline())
        except:
            self.min_price = 0
            self.max_price = 10**9 # a billion...

    def process_item(self, item, spider):
        ids_to_remove = []
        for id in item:
            # try:
            #     if item[id]['title'].encode('utf-8').strip() is not in self.car_filter
            # except:
            #     title = 'N/A'
            try:
                price = int(item[id]['price'].replace('$',''))
            except:  # price doesn't exist
                price = None
                ids_to_remove.append(id)
            if price is not None:
                if self.max_price < price or self.min_price > price:
                    ids_to_remove.append(id)

        # remove items that did not get past filters
        for id in ids_to_remove:
            del item[id]

        return item


# stage 2: store data in csv file
class CarawlerCSVPipeline(object):

    def process_item(self, item, spider):
        with open('carawler/output/cars.csv', 'wb') as f:
            self.csvwriter = csv.writer(f, delimiter=',')
            self.csvwriter.writerow(['Count', 'ID', 'Post Title', 'Price', 'Location', 'URL'])
            for id in item:
                count = item[id]['count']
                try:
                    title = item[id]['title'].encode('utf-8').strip()
                except:
                    title = 'N/A'
                try:
                    price = item[id]['price'].encode('utf-8').strip()
                except:
                    price = 'N/A'
                try:
                    location = item[id]['location'].encode('utf-8').strip()
                except:
                    location = 'N/A'
                try:
                    url = item[id]['url'].encode('utf-8').strip()
                except:
                    url = 'N/A'
                self.csvwriter.writerow([count, id, title, price, location, url])

        return item

# stage 3: convert csv to xlsx to store data in more readable format
class CarawlerConvertToSpreadsheetPipeline(object):

    def __init__(self):
        self.csvfilename = 'carawler/output/cars.csv'
        self.spreadsheetfilename = 'carawler/output/cars.xlsx'

    def process_item(self, item, spider):
        wb = Workbook()
        ws = wb.active
        ws.title = "Cars"
        with open(self.csvfilename, 'r') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader, start=1):
                for c, val in enumerate(row, start=1):
                    ws.cell(row=r, column=c).value = val
        wb.save(self.spreadsheetfilename)

        return item