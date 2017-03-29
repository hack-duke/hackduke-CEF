import scrapy
from housing.items import HousingItem

class ZillowSpider(scrapy.Spider):
    name = "zillow"


    def start_requests(self):
        zipcodes = ["27708", "27517", "27702", "27705", "27708", "27711", "27715", "27560", "27703", "27706", "27709", "27712", "27717", "27701", "27704", "27707", "27710", "27713"]    
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
                item['price'] = sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract()[0]
                datePt1 = sel.xpath('.//span[@class="toz-count"]/text()').extract()[0]
                datePt2 = sel.xpath('.//span[@class="zsg-photo-card-notification toz "]/text()').extract()[0]
                item['dateListed'] = datePt1 + datePt2
                item['address'] = sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract()[0]
                item['specs'] = ''.join(sel.xpath('.//span[@class="zsg-photo-card-info"]/text()').extract())
                item['url'] = "zillow.com" + sel.xpath('.//a[@class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"]/@href').extract()[0]
                if int(removeCharacters(item['price'], ["$", ",", "/mo"])) < 1500:
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

