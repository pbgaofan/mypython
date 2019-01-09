# -- coding:utf-8 --

import pymysql
import requests
from bs4 import BeautifulSoup
import time



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}


class GetIp:
    def __init__(self):
        config = {

            'host': 'localhost',
            'port': 3306,
            'user': 'honest',
            'passwd': 'Yule1919~!@',
            'db': 'IPS',
            'charset': 'utf8'
        }
        conn = pymysql.Connect(**config)
        self.conn = conn
        self.cursor = self.conn.cursor()

    def close_connection(self):
        self.conn.close()

    def repitition(self,proxy):
        sql='select * from kuaidaili where proxy="{}"'.format(proxy)
        self.cursor.execute(sql)
        if self.cursor.fetchone():
            return True
        return False

    # 爬取ip主函数
    def crawl_ip(self):
        print('www.kuaidaili.com代理爬取启动...')
        count = 0
        # 爬取两页的ip，然后调用check_ip判断ip有效性，有效则插入到数据库中
        urls=['https://www.kuaidaili.com/free/inha/1/','https://www.kuaidaili.com/free/intr/']
        for url in urls:
            html = requests.get(url, headers=headers).text
            soup = BeautifulSoup(html, 'lxml')
            table=soup.find('table')
            trs=table.tbody.find_all('tr')
            for tr in trs:
                ip=tr.find_all('td')[0].get_text().strip()
                port=tr.find_all('td')[1].get_text().strip()
                ip_type=tr.find_all('td')[3].get_text().strip().lower()
                proxy=ip_type+r'://'+ip+':'+port
                anonymous=tr.find_all('td')[2].get_text()
                if not self.repitition(proxy):
                    sql = 'insert into kuaidaili (proxy,annoy) values ("{0}","{1}")'.format(proxy, anonymous)
                    self.cursor.execute(sql)
                    self.conn.commit()
                    count+=1
            time.sleep(3)

        print('爬取结束，供爬取了{}个代理'.format(count))


get_ip_instance = GetIp()
get_ip_instance.crawl_ip()
