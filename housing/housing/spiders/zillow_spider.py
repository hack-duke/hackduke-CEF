import scrapy
from housing.items import HousingItem
import urllib.request
import json

# https://www.zipcodeapi.com/API for more info on zip api

class ZillowSpider(scrapy.Spider):
    name = "zillow"

    def __init__(self, city='Durham', state='NC', limit=100000000, *args, **kwargs):
        super(ZillowSpider, self).__init__(*args, **kwargs)
        self.city = city.replace('-', ' ')
        self.state = state
        self.limit = int(limit)


    def start_requests(self):
        api_key = "c9yS4jXsBsAMAIAcm4hYBaztIh4aFwZRGxJKRHds9OeJwPWTUdRvorZ7J3iozhff"
        city = self.city
        state = self.state
        url = "https://www.zipcodeapi.com/rest/" + api_key + "/city-zips.json/" + city + "/" + state
        response = urllib.request.urlopen(url)
        data = json.load(response)
        zipcodes = data['zip_codes']

        urls = [ ]

        for code in zipcodes:
            urls.append("https://www.zillow.com/homes/for_rent/" + code)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//ul[@class="photo-cards"]/li'):
            try:
                item = HousingItem()
                item['classification'] = sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract()[0]
                priceInfo = sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract()[0]
                item['pricePerMonth'] = removeCharacters(priceInfo, ["$", ",", "/mo"])
                datePt1 = sel.xpath('.//span[@class="toz-count"]/text()').extract()[0]
                datePt2 = sel.xpath('.//span[@class="zsg-photo-card-notification toz "]/text()').extract()[0]
                item['dateListed'] = datePt1 + datePt2
                item['address'] = sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract()[0]
                item['specs'] = ''.join(sel.xpath('.//span[@class="zsg-photo-card-info"]/text()').extract())
                item['url'] = "zillow.com" + sel.xpath('.//a[@class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"]/@href').extract()[0]
                if int(item['pricePerMonth']) <= self.limit:
                    yield item
            except:
                pass
        next_page = sel.xpath('//li[@class="zsg-pagination-next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = "https://zillow.com" + next_page
            yield scrapy.Request(next_page, self.parse)

def removeCharacters(string, removalList):
    newstring = string
    for item in removalList:
        newstring = newstring.replace(item, '')
    return newstring

