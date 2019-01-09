# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class LianjiaBeijingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    platform = Field()
    district = Field()
    microdistrict = Field()
    district_unit_price = Field()
    house_num = Field()
    year = Field()
    deal_total_num = Field()
    house_deal_money = Field()
    house_area = Field()
    date = Field()
    house_unit_price = Field()
