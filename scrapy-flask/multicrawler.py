import scrapy
from scrapy.crawler import CrawlerProcess
from housing.spiders.show_me_the_rent import ShowMeTheRentSpider
from housing.spiders.zillow_spider import ZillowSpider
from housing.spiders.CAL import CheapApartmentsLocatorSpider as CALSpider
import sys
import csv
import operator
import os
import json

def get_json():
    filename = 'output.json'
    clean(filename)
    process = CrawlerProcess({
    'FEED_URI': filename,
    'FEED_FORMAT': 'jsonlines'
    })
    crawl(process)
    return extract_json(filename)

def get_csv():
    filename = 'output.csv'
    clean(filename)
    process = CrawlerProcess({
    'FEED_URI': filename,
    'FEED_FORMAT': 'csv'
    })
    crawl(process)
    return extract_csv(filename)

def crawl(process):
    spider1 = ShowMeTheRentSpider()
    spider2 = ZillowSpider()
    spider3 = CALSpider()
    process.crawl(spider1)
    process.crawl(spider2)
    process.crawl(spider3)
    process.start()

def extract_json(filename):
    with open(filename) as data_file: 
        data = []   
        for line in data_file:
            data.append(line)
    return {'data': data}

def extract_csv(filename):
    with open(filename) as data_file:    
        data = data_file.read()
    return {'data': data}

def sort():
    cols = []
    keys = []
    reader = csv.reader(open("output.csv"), delimiter=",")
    for row in reader:
        try:
            float(row[3])
            cols.append(row)
        except ValueError:
            keys.append(row)

    cols.sort(key=lambda x: float(x[3]))
    writeData(keys, cols)

def writeData(keys, cols):
    clean('sortedOutput.csv')
    with open('sortedOutput.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(keys)
        for col in cols:
            writer.writerow(col)

def clean(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

if __name__ == "__main__":
    main()
 #   sort()
 #   clean('output.csv')