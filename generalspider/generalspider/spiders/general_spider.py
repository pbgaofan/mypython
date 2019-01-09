import scrapy
from bs4 import BeautifulSoup
import os


class GeneralSpider(scrapy.Spider):
    name = 'generalspider'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):

        movies=response.xpath('//*div[@class="info"]')
        for movie in movies:
            title=movie.xpath('//div[@class="hd"]/a/span/text()').extract()
            print('-'*50)
            print(title)