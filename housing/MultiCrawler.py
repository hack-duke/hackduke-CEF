import scrapy
from scrapy.crawler import CrawlerProcess
from housing.spiders.show_me_the_rent import ShowMeTheRentSpider
from housing.spiders.zillow_spider import ZillowSpider
from housing.spiders.CAL import CheapApartmentsLocatorSpider as CALSpider
import sys
import csv
import operator
import os

def main():
    try:
        os.remove('output.csv')
    except FileNotFoundError:
        pass
    process = CrawlerProcess({
    'FEED_URI': 'output.csv',
    'FEED_FORMAT': 'csv'
    })
    spider1 = ShowMeTheRentSpider()
    spider2 = ZillowSpider()
    spider3 = CALSpider()
    process.crawl(spider1)
    process.crawl(spider2)
    process.crawl(spider3)
    process.start()
    sort()

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
    try:
        os.remove('sortedOutput.csv')
    except FileNotFoundError:
        pass
    house_data = open('sortedOutput.csv', 'w')
    csvwriter = csv.writer(house_data)
    csvwriter.writerow(keys[0])
    for i in range(len(cols)):
        csvwriter.writerow(cols[i])

    house_data.close()

if __name__ == "__main__":
    main()
    sort()