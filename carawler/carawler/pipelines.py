# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, csv, os
from scrapy.exporters import CsvItemExporter
from openpyxl import Workbook

class CarawlerFilterPipeline(object):
    def process_item(self, item, spider):
        return item


class CarawlerCSVPipeline(object):

    def __init__(self):
        self.csvwriter = csv.writer(open('carawler/output/cars.csv', 'wb'), delimiter=',')
        self.csvwriter.writerow(['ID', 'Post Title', 'Price', 'Location', 'URL']) #, 'starts', 'subjects', 'reviews'])

    def process_item(self, item, spider):
        print("-----------------------------------------------process_item - item --------------------------------------------------")
        print(item)
        print("-----------------------------------------------process_item - logic --------------------------------------------------")
        for i in xrange(0, len(item)):
            print("-----------------------------------------------process_item - i value --------------------------------------------------")
            print(i)
            row = item[i]
            id = row['id']
            try:
                title = row['title'].encode('utf-8').strip()
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
            self.csvwriter.writerow([id, title, price, location, url])

        return item

class CarawlerConvertToSpreadsheetPipeline(object):

    def __init__(self):
        self.csvwriter = csv.reader(open('carawler/output/cars.csv', 'rb'), delimiter=',')
        self.csvfilename = 'carawler/output/cars.csv'
        self.spreadsheetfilename = 'carawler/output/cars.xlsx'

    def process_item(self, item, spider):
        wb = Workbook()
        ws = wb.active
        ws.title = "Cars"
        with open(self.csvfilename, 'rb') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader, start=1):
                for c, val in enumerate(row, start=1):
                    ws.cell(row=r, column=c).value = val
        wb.save(self.spreadsheetfilename)

        return item