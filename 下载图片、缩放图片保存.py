# -*- coding:utf-8 -*-   声明文件编码
import sys
from PIL import Image
import xlrd
import xlwt
import json
import requests
import os

#http://img.pb89.com/AppProductImg/B1HA71318/LIST/1.jpg
def Downloda_img(excel_path,column,root_path):                   #下载图片到本地
    workbook=xlrd.open_workbook(excel_path)
    sheet1=workbook.sheets()[0]
    valid_col3=sheet1.col_values(column)[1:]
    g=(root_path+'/'+x for x in valid_col3)
    for x in g:
        if not x==root_path+'/':
            url_split=x.split('/')
            save_dir='D:\\test\\'+url_split[-3]+'\\'+url_split[-2]+'\\'
            pic=requests.get(x)
            if not os.path.isdir(save_dir):
                os.makedirs(save_dir)
            with open(save_dir+url_split[-1],'wb') as f:
                f.write(pic.content)
def change_size(dirr,width):                                               #改变尺寸，并保存
    if os.path.isdir(dirr):
        for root,dirs,filelist in os.walk(dirr):
            for filename in filelist:
                if filename.split('.')[1] in ['jpg','png']:
                    im=Image.open(os.path.join(root,filename))
                    (x,y)=im.size
                    new_x=int(width)
                    new_y=int(width*y/x)
                    out=im.resize((new_x,new_y),Image.ANTIALIAS)
                    save_path='\\'.join(root.split('\\')[0:-1])
                    if not os.path.isdir(save_path+'\\'+'thumbnail'):
                        os.makedirs(save_path+'\\'+'thumbnail')
                    out.save(save_path+'\\'+'thumbnail\\'+filename)

excel_path='D:\\test\\tmp001.xls'
column=9
root_path='http://img.pb89.com'
dirr='D:\\test'
width=400

Downloda_img(excel_path,column,root_path)
change_size(dirr,width)
