# -*- coding: utf-8 -*-

import os
import io
import sys
import requests
from lxml import etree
import smtplib
import email.mime.multipart
import email.mime.text
from urllib import request
import pymysql
import time

dir_r=r'D:\novel'
base_url='https://tieba.baidu.com/p/5003417923'
data={
'pn':1
}
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
}


def sendmail(page_num):

    url=base_url+'?pn='+str(page_num)
    msg = email.mime.multipart.MIMEMultipart()

    msg['Subject'] = '小说更新提醒'
    msg['From'] = '15355135297@163.com'
    msg['To'] = '634019948@qq.com'
    content = '''
    小说已经更新啦，快去看看吧，链接如下：
    {}

    '''.format(url)
    txt = email.mime.text.MIMEText(content)
    msg.attach(txt)

    #smtp = smtplib
    smtp = smtplib.SMTP()
    smtp.connect('smtp.163.com', '25')
    smtp.login('15355135297@163.com', 'mhwl2017')
    smtp.sendmail('15355135297@163.com', '634019948@qq.com', msg.as_string())
    smtp.quit()

class Database(object):
    config={
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'passwd':'root',
    'db':'app',
    'charset':'utf8'
    }
    global cursor,conn
    conn=pymysql.connect(**config)
    cursor=conn.cursor()
    sql='select * from app order by add_time desc limit 1'
    cursor.execute(sql)
    result=cursor.fetchall()
    current_floor=result[0][0]
    current_page=result[0][1]
    def addItems(self,page,floor):
        sql='insert into app (current_page,current_floor ) values({},{}) '.format(page,floor)
        cursor.execute(sql)
        conn.commit()
    def closeConn(self):
        conn.close()
def inti(base_url):
    r=requests.get(base_url,params=data,headers=headers)
    html=r.text
    selector=etree.HTML(html)
    biggest_page=selector.xpath("//*[@id='thread_theme_5']/div[1]/ul/li[2]/span[2]/text()")
    biggest_page=int(biggest_page[0])
    data1={
    'pn':biggest_page
    }
    selector1=etree.HTML(requests.get(base_url,params=data1,headers=headers).text)
    last_floor=selector1.xpath("//div[@class='louzhubiaoshi_wrap']/../following-sibling::div[1]//span[@class='tail-info']/text()")[-2][0:-1]
    last_floor=int(last_floor)
    current_floor=Database().current_floor
    current_page=Database().current_page
    print(current_floor,current_page)
    if biggest_page>current_page:
        sendmail(current_page)
        Database().addItems(biggest_page,last_floor)
    if biggest_page==current_page:
        if current_floor<last_floor:
            sendmail(current_page)
            Database().addItems(biggest_page,last_floor)
i=1
while True:
    inti(base_url)
    print('program executed {} times'.format(i))
    time.sleep(60)
    i+=1
