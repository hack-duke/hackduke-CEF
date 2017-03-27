# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classification = scrapy.Field()
    price = scrapy.Field()
    dateListed = scrapy.Field()
    address = scrapy.Field()
    specs = scrapy.Field()
    url = scrapy.Field()
    pass
