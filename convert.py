import csv 
import openpyxl
import os


class Convert():

    def __init__(self):
        self.process_dir=os.path.dirname(os.getcwd())

    def csv_to_xlsx(self):
        i=0
        for root,dirlist,filelist in os.walk(self.process_dir):
            for filename in filelist:
                ext=filename.split('.')[-1]
                if ext=='csv':
                    print('正在处理{}...'.format(filename))
                    i+=1
                    filepath=os.path.join(root,filename)
                    workbook=openpyxl.Workbook()
                    wst=workbook.active
                    with open(filepath,'r') as f:
                        read=csv.reader(f)
                        for line in read:
                            wst.append(line)
                    filename=os.path.split(filepath)[1].split('.')[0]+'.xlsx'
                    newfilepath=os.path.join(root,filename)
                    workbook.save(newfilepath)
                    os.remove(filepath)
                    print('{}已处理完成...'.format(filename))
        print('共处理了{}个csv文件....'.format(i))
        input('按任意键退出...')
        return

csv2xlsx=Convert()
csv2xlsx.csv_to_xlsx()
