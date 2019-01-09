import pymysql
import requests
from bs4 import BeautifulSoup
import time
import datetime


class Mysql():
    def __init__(self):
        config={
        'host':'localhost',
        'port':3306,
        'user':'root',
        'passwd':'Yule1919~!@',
        'db':'dev',
        'charset':'utf8'
        }
        self.conn=pymysql.Connect(**config)
        self.cursor=self.conn.cursor()

    def isexist(self,opinion):
        self.cursor.execute('select * from huxiuopinion where opinion="{}"'.format(opinion))
        results=self.cursor.fetchall()
        if not results:
            return False
        return True

    def insert(self,author,opinion):

        if not self.isexist(opinion):
            sql='insert into huxiuopinion (author,opinion) values ("{}","{}")'.format(author,opinion)
            self.cursor.execute(sql)
            self.conn.commit()

    def close(self):
        self.conn.close()

url='https://www.huxiu.com/moment'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
mysql=Mysql()

while 1:
    html=requests.get(url,headers=headers).text
    soup=BeautifulSoup(html,'lxml')
    news_list=soup.find(id='mt-list-root').find_all('li','mt-list')
    for news in news_list:
        author=news.div.div.span.a.text
        opinion=news.p.text
        mysql.insert(author,opinion)
        print('insert sucess --{}'.format(datetime.datetime.now()))
    time.sleep(300)
