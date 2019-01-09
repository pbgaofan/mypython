#coding=utf-8
import os
import sys
import string
import time



#f方法1，递归
'''
def showallfiles(path,allfile):

    formart='0123456789'
    if os.path.isdir(path):
        filelist=os.listdir(path)
        for filename in filelist:
            filepath=os.path.join(path+'/',filename)
            if os.path.isdir(filepath):
                showallfiles(filepath,allfile)
            else:
                split_filepath=os.path.split(filepath)
                file_ext=split_filepath[-1].split('.')[0]
                file_type=split_filepath[-1].split('.')[-1]
                for every_letter in file_ext:
                    if every_letter not in formart:
                        file_ext=file_ext.replace(every_letter,'')
                new_filepath=split_filepath[0]+'/'+file_ext+'.'+file_type
                allfile.append(new_filepath)
                try:
                    os.rename(filepath,new_filepath)
                except Exception,e:
                    print e
    else:
        allfile.append(path)

    return allfile

print showallfiles('D:/test/',[])

'''
#方法2，利用os.walk遍历
def change_words(path):

    formart='0123456789'
    if os.path.isdir(path):
        dir_g=os.walk(path)
        for root,dirlist,filelist in dir_g:
            for file_fullname in filelist:
                file_name=file_fullname.split('.')[0]
                file_type=file_fullname.split('.')[1]
                oldpath=os.path.join(root,file_fullname)
                for x in file_name:
                    if x not in formart:
                        file_name=file_name.split('.')[0].replace(x,'')
                new_file_fullname=file_name+'.'+file_type
                newpath=os.path.join(root,new_file_fullname)
                try:
                    os.rename(oldpath,newpath)
                except FileExistsError:
                    print('没有需要替换哒')

start=time.time()
change_words('D:\\test')
end=time.time()
print( '运行成功\n运行时间{}秒'.format((end-start)))
