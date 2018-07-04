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
class CarawlerFilterPipeline(object):

    # open filter files if they exist
    def __init__(self):
        self.car_filter_filename = 'carawler/input/car_filter.txt'
        self.price_filter_filename = 'carawler/input/price_filter.txt'
        try:
            self.car_filter = open(self.car_filter_filename, 'rb')
        except:
            self.car_filter = None
        try:
            self.price_filter = open(self.price_filter_filename, 'rb')
        except:
            self.price_filter = None

    def process_item(self, item, spider):
        for i in xrange(0, len(item)):
            row = item[i]
            id = row['id']
            try:
                title = row['title'].encode('utf-8').strip().lower()
                if title not in self.car_filter.readlines().lower():
                    pass
            except:
                title = 'N/A'
            try:
                price = row['price'].encode('utf-8').strip()
            except:
                price = 'N/A'
            try:
                location = row['location'].encode('utf-8').strip()
            except:
                location = 'N/A'
            try:
                url = row['url'].encode('utf-8').strip()
            except:
                url = 'N/A'

        if self.car_filter is not None:
            self.car_filter.close()
        if self.price_filter is not None:
            self.price_filter.close()

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