# -*- coding: utf-8 -*-
import scrapy
from housing.items import HousingItem
import urllib.request
import json


class CheapApartmentsLocatorSpider(scrapy.Spider):
    name = "CAL"

    def __init__(self, *args, **kwargs):
        super(CheapApartmentsLocatorSpider, self).__init__(*args, **kwargs)
        self.limit = 20000
        self.num = 0

    def start_requests(self):
        city = 'durham'
        urls = ['http://www.cheapapartmentslocator.com/cheap-apartments-in-' + city + '/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//div[@class="apartmentTable"]/div[@class="rightCol"]'):
            try:
                item = HousingItem()
                item['classification'] = 'for rent'
                tableHeader = sel.xpath('.//table[@class="fpBox"]/tr/th/text()').extract()
                tableContents = sel.xpath('.//table[@class="fpBox"]/tr/td[@class="even"]/text()').extract()
                item['specs'] = tableHeader[0] + " " + tableContents[0] + ", " + tableHeader[1] + " " + tableContents[1]
                item['pricePerMonth'] = tableContents[-1].replace("$ ", "").replace(",", "")
                item['dateListed'] = 'unknown'
                streetAddress = sel.xpath('.//p[@class="apartmentAdd"]/text()').extract_first()
                item['address'] = streetAddress.split('-')[0].replace('\n', '').replace('\t', '')
                item['url'] = sel.xpath('.//h2/a[@class="apartmentName  external"]/@href').extract_first()
                if item['url'] is None:
                    item['url'] = response.url
                if int(item['pricePerMonth']) <= self.limit:
                    self.num = self.num + 1
                    yield item
            except:
                pass

        nextPagesList = sel.xpath('//ul[@class="page"]/li/a/@href').extract()
        for next_page in nextPagesList:
            yield scrapy.Request("http://www.cheapapartmentslocator.com" + next_page, self.parse)
