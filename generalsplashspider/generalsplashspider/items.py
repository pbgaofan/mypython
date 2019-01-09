# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GeneralsplashspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    nickname=scrapy.Field()
    follow_count=scrapy.Field()
    funs_count=scrapy.Field()
    liveroom_url=scrapy.Field()
    anchor_flag=scrapy.Field()
    user_level=scrapy.Field()
