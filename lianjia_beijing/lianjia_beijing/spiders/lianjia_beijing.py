import scrapy
from lianjia_beijing.items import LianjiaBeijingItem
from scrapy import Selector
from urllib.parse import quote


class LianjiaBeijinSpider(scrapy.Spider):
    name = 'lianjiabj'

    dic = {
        '朝阳': {
            '北苑': 'beiyuan2',
            '北工大': 'beigongda',
            '百子湾': 'baiziwan',
            '常营': 'changying',
            'CBD': 'cbd',
            '朝青': 'chaoqing',
            '朝阳公园': 'chaoyanggongyuan',
            '东坝': 'dongba',
            '大望路': 'dawanglu',
            '东大桥': 'dongdaqiao',
            '大山子': 'dashanzi',
            '豆各庄': 'dougezhuang',
            '定福庄': 'dingfuzhuang',
            '垡头': 'fatou',
            '工体': 'gongti',
            '高碑店': 'gaobeidian',
            '国展': 'guozhan1',
            '甘露园': 'ganluyuan',
            '管庄': 'guanzhuang',
            '欢乐谷': 'huanlegu',
            '惠新西街': 'huixinxijie',
            '红庙': 'hongmiao',
            '华威桥': 'huaweiqiao',
            '健翔桥': 'jianxiangqiao1',
            '酒仙桥': 'jiuxianqiao',
            '劲松': 'jinsong',
            '建国门外': 'jianguomenwai',
            '农展馆': 'nongzhanguan',
            '南沙滩': 'nanshatan1',
            '潘家园': 'panjiayuan1',
            '三元桥': 'sanyuanqiao',
            '芍药居': 'shaoyaoju',
            '石佛营': 'shifoying',
            '十里堡': 'shilibao',
            '首都机场': 'shoudoujichang1',
            '双井': 'shuangjing',
            '十里河': 'shilihe',
            '十八里店': 'shibalidian1',
            '双桥': 'shuangqiao',
            '三里屯': 'sanlitun',
            '四惠': 'sihui',
            '团结湖': 'tuanjiehu',
            '太阳宫': 'taiyanggong',
            '甜水园': 'tianshuiyuan',
            '望京': 'wangjing',
            '西坝河': 'xibahe',
            '亚运村': 'yayuncun',
            '亚运村小营': 'yayuncunxiaoying',
            '中央别墅区': 'zhongyangbieshuqu1',
            '朝阳其他': 'zhaoyangqita'
        },
        '通州': {
            '北关': 'beiguan',
            '果园': 'guoyuan1',
            '九棵树': 'jiukeshu12',
            '潞苑': 'luyuan',
            '梨园': 'liyuan',
            '临河里': 'linheli',
            '乔庄': 'qiaozhuang',
            '通州北苑': 'tongzhoubeiyuan',
            '通州其他': 'tongzhouqita11',
            '武夷花园': 'wuyihuayuan',
            '新华大街': 'xinhuadajie',
            '亦庄': 'yizhuang1',
            '玉桥': 'yuqiao'
        }
    }

    dic = {'朝阳': {'北苑': 'beiyuan2'}}
    base_url = 'https://bj.lianjia.com/xiaoqu/{}/'

    def start_requests(self):
        for district, mini_dic in self.dic.items():
            meta = {'platform': '链家', 'district': district}
            for x in mini_dic.values():
                url = self.base_url.format(x)
                yield scrapy.Request(
                    url, callback=self.parse_page_num, meta=meta)

    def parse_page_num(self, response):
        sel = Selector(response)
        try:
            page_num_dict = sel.xpath(
                '//div[@class="page-box house-lst-page-box"]/@page-data'
            ).extract()[0]
            page_num = eval(page_num_dict)['totalPage']
        except Exception:
            page_num = 1
        meta = response.meta
        page_num = int(page_num)
        for num in range(1, page_num + 1):
            url = response.url + 'pg{}/'.format(num)
            yield scrapy.Request(url, callback=self.parse_list, meta=meta)


# 小区均价，户数，建成年代，成交总套数，具体成交金额，面积，日期，均价。

    def parse_list(self, response):
        sel = Selector(response)
        houselis = sel.xpath('//div[@class="info"]')
        for houseli in houselis:
            meta = response.meta
            title = houseli.xpath('.//div[@class="title"]/a/text()').extract()[
                0]
            url = houseli.xpath('.//div[@class="title"]/a/@href').extract()[0]
            district_unit_price = houseli.xpath(
                './/div[@class="totalPrice"]/span/text()').extract()[0]
            year = houseli.xpath(
                './/div[@class="positionInfo"]/text()').extract()[0]
            meta['microdistrict'] = title
            meta['district_unit_price'] = district_unit_price
            meta['year'] = year
            print('-' * 50)
            print(meta)
            #yield scrapy.Request(
            #url, callback=self.parse_detail, meta=response.meta)
            break

    def parse_detail(self, response):
        sel = Selector(response)
        house_num = sel.xpath(
            '//div[@class="xiaoquInfo"]/div[7]/span[2]/text()').extract()[0]
        year = sel.xpath(
            '//div[@class="xiaoquInfo"]/div[1]/span[2]/text()').extract()[0]
        print(response.meta)
        print(district_unit_price)
        print(house_num)
        print(year)

    def parse_deal(self, response):
        pass
