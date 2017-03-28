import scrapy
from housing.items import HousingItem

# https://www.youtube.com/watch?v=A4949-hT8TM

class ZillowSpider(scrapy.Spider):
    name = "zillow"


    def start_requests(self):
        zipcodes = ["27708", "27517", "27702", "27705", "27708", "27711", "27715", "27560", "27703", "27706", "27709", "27712", "27717", "27701", "27704", "27707", "27710", "27713"]    
        urls = [ ]

        for code in zipcodes:
            urls.append("https://www.zillow.com/homes/for_rent/" + code + "_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=rent")

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
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
                items.append(item)
            except:
                pass
        return items
