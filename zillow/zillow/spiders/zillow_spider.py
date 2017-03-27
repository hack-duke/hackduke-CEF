import scrapy
from zillow.items import ZillowItem

# https://www.youtube.com/watch?v=A4949-hT8TM

class ZillowSpider(scrapy.Spider):
    name = "zillow"

    def start_requests(self):
        urls = [
            "https://www.zillow.com/homes/for_rent/Warrenton-VA-20186/house,condo,apartment_duplex,mobile,townhouse_type/66272_rid/38.774161,-77.630424,38.63645,-78.069878_rect/10_zm/",
            "https://www.zillow.com/homes/for_rent/27708_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=rent"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = []
        for sel in response.xpath('//ul[@class="photo-cards"]/li'):
            try:
                item = ZillowItem()
                print(type(item))
                item['classification'] = sel.xpath('.//span[@class="zsg-photo-card-status"]/text()').extract()[0]
                print(item['classification'])
                item['price'] = sel.xpath('.//span[@class="zsg-photo-card-price"]/text()').extract()[0]
                print(item['price'])
                datePt1 = sel.xpath('.//span[@class="toz-count"]/text()').extract()[0]
                datePt2 = sel.xpath('.//span[@class="zsg-photo-card-notification toz "]/text()').extract()[0]
                item['dateListed'] = datePt1 + datePt2
                print(item['dateListed'])
                item['address'] = sel.xpath('.//span[@class="zsg-photo-card-address"]/text()').extract()[0]
                print(item['address'])
                item['specs'] = ''.join(sel.xpath('.//span[@class="zsg-photo-card-info"]/text()').extract())
                print(item['specs'])
                totalUrl = "zillow.com" + (sel.xpath('.//a[@class="zsg-photo-card-overlay-link routable hdp-link routable mask hdp-link"]/@href').extract())[0]
                item['url'] = totalUrl
                print(item['url'])
                items.append(item)
            except:
                pass
        return items
