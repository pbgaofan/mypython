import scrapy
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
import re
from generalsplashspider.items import GeneralsplashspiderItem


class GeneralSplashSpider(scrapy.Spider):
    name = 'generalsplashspider'
    start_urls=[]
    for i in range(1,100000):
        start_urls.append('https://yuba.douyu.com/user/main/{}'.format(i))
    '''
    for i in range(1, 108, 2):

        url = 'https://search.jd.com/Search?keyword=%E5%85%BB%E7%94%9F%E5%A3%B6&enc=utf-8&qrst=1&rt=1&stop=1&spm=1.1.5&vt=2&stock=1&page={0}&s=1&click=0'.format(
            i)
        start_urls.append(url)
    '''
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        soup=BeautifulSoup(response.body,'html5lib')
        url=response.url
        print('url: '+url)
        try:
            nickname=soup.find('h1','personal_head-userName-fPo6k').get_text()
        except Exception:
            nickname=''
            follow_count=''
            funs_count=''
            liveroom_url=''
            anchor_flag=''
            user_level=''
        follow_count=soup.find('span','index-HeaderCount-hQ86V').get_text()
        funs_count=soup.find_all('span','index-HeaderCount-hQ86V')[1].get_text()
        try:
            liveroom_url=soup.find('div','liveroom-wrapper-3ORke').a.get('href')
        except Exception:
            liveroom_url=''
        try:
            anchor_flag=soup.find('div','index-badge-_31SH').img.get('alt')
            anchor_flag='Y'
        except Exception:
            anchor_flag='N'
        user_level=re.findall('\d+',soup.find('div','index-badge-_31SH').find_all('img',attrs={'alt':'等级'})[0].get('src'))[0]
        item=GeneralsplashspiderItem()
        item['url']=url
        item['nickname']=nickname
        item['follow_count']=follow_count
        item['funs_count']=funs_count
        item['liveroom_url']=liveroom_url
        item['anchor_flag']=anchor_flag
        item['user_level']=user_level
        yield item
        
