# -*- coding: utf-8 -*-
import scrapy
from housing.items import HousingItem
import urllib.request
import json


class ShowMeTheRentSpider(scrapy.Spider):
    name = "show_me_the_rent"

    def __init__(self, *args, **kwargs):
        super(ShowMeTheRentSpider, self).__init__(*args, **kwargs)
        self.limit = 20000

    def start_requests(self):
        zipcode = '10024'
        urls = ['https://www.showmetherent.com/listings/' + zipcode]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for sel in response.xpath('//div[@class="listing-table"]/div'):
            try:
                item = HousingItem()
                item['classification'] = trimSlashes(sel.xpath('.//div[@class="c3 listing-secondary"]/p[@class="listing-numunits"]/text()').extract_first())
                item['specs'] = sel.xpath('.//div[@class="c3 listing-secondary"]/p[@class="listing-bedrooms"]/text()').extract_first()
                item['pricePerMonth'] = stripPrice(sel.xpath('.//div[@class="c4 listing-rent-wrapper"]/p[@class="listing-rent"]/text()').extract_first())
                item['dateListed'] = trimSlashes(sel.xpath('.//div[@class="c3 listing-secondary"]/p[@class="listing-lastupdate"]/text()').extract_first())
                streetAddress = sel.xpath('.//div[@class="c2 listing-name"]/h2/a/text()').extract_first()
                city = trimSlashes(sel.xpath('.//div[@class="c2 listing-name"]/h3/text()').extract_first())
                item['address'] = streetAddress + ', ' + city
                item['url'] = 'www.showmetherent.com' + sel.xpath('.//div[@class="c2 listing-name"]/h2/a/@href').extract_first()
                if int(item['pricePerMonth']) <= self.limit:
                    print(item['pricePerMonth'])
                    yield item
            except:
                pass

        nextPagesList = sel.xpath('//div[@class="page_bar"]/a')
        next_page = nextPagesList[len(nextPagesList) - 1].xpath('.//@href').extract_first()
        if next_page is not None:
            next_page = "https://www.showmetherent.com" + next_page
            yield scrapy.Request(next_page, self.parse)

def trimSlashes(string):
    if '\n' or '\r' or '\t' or '\u00bd' in string:
        string = string.replace('\n', '').replace('\r', '').replace('\t', '').replace('\u00bd', '')
        string = string.rstrip().lstrip()
    return string

def stripPrice(string):
    if '-' in string:
        string = string[0:string.index('-')]
    string = string.replace('$', '').replace(',', '')
    return string

def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False
