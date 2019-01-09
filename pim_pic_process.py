import os
import re
dir_temp = r'F:\MG PIM图片处理'
new_dir = r'F:\MG PIM图片处理\result'

'''
for root, dir_names, file_names in os.walk(dir_temp):
    for file_name in file_names:
        if re.findall(' ', file_name):
            old_file_path = os.path.join(root, file_name)
            new_name = re.sub(' ', '', file_name)
            #new_file_path=os.path.join(root,new_name)
            new_file_path = os.path.join(new_dir,
                                         os.path.join('\\'.join(
                                             old_file_path.split('\\')[2:-1]),
                                                      new_name))
            tmp_dir = os.path.split(new_file_path)[0]
            if not os.path.isdir(tmp_dir):
                os.makedirs(tmp_dir)
            #os.rename(old_file_path, new_file_path)
            print('/'.join(old_file_path.split('\\')[2:]), ',', '/'.join(
                new_file_path.split('\\')[2:]))
'''

def find_chinese():
    for root, dir_names, file_names in os.walk(dir_temp):
        print(file_names)
        for file_name in file_names:
            if not re.findall('[A-Za-z0-9\._\-]+', file_name):
                print(file_name)


find_chinese()
