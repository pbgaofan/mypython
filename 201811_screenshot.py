# -*- coding:utf-8 -*-
from selenium import webdriver
import os
import time

url = 'http://192.168.20.25:8039/?tdsourcetag=s_pctim_aiomsg'

dir_root = r'D:\2018双十一截屏'
lis_name = [
    'total', 'pbmen', 'pbwomen', 'ledin', 'mg', 'mini', 'pt', 'ledinhome'
]
for name in lis_name:
    brand_dir = os.path.join(dir_root, name)
    if not os.path.isdir(brand_dir):
        os.makedirs(brand_dir)
#executable_path = os.path.join(sys.path[0], 'geckodriver.exe')
#browser = webdriver.Firefox(executable_path=executable_path)
executable_path = os.path.join(dir_root, 'chromedriver.exe')
browser = webdriver.Chrome(executable_path=executable_path)
length = len(lis_name)
#dic = {lis_name[i]: {num: 0 for num in lis[i]} for i in range(length)}

lis_id = [
    'p_100', 'p_173275708', 'p_112394247', 'p_513051429', 'p_2002445600',
    'p_1683598224', 'p_3847939733', 'p_3718986362'
]

dic_id = {lis_name[i]: lis_id[i] for i in range(length)}

browser.get(url)
time.sleep(5)
browser.refresh()
time.sleep(5)


def now():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())


def get_amount(_id):
    if _id == 'p_100':
        return int(
            browser.find_element_by_id(_id).get_attribute('value').replace(
                ',', ''))
    return int(browser.find_element_by_id(_id).text.replace(',', ''))


"""
total_amount = get_amount('p_100')
pbmen_amount = get_amount('p_173275708')
pbwomen_amount = get_amount('p_112394247')
ledin_amount = get_amount('p_513051429')
mg_amount = get_amount('p_2002445600')
mini_amount = get_amount('p_1683598224')
pt_amount = get_amount('p_3847939733')
ledinhome_amount = get_amount('p_3718986362')
amount_lis = [
    total_amount, pbmen_amount, pbwomen_amount, ledin_amount, mg_amount,
    mini_amount, pt_amount, ledinhome_amount
]y
 """
dic_path = os.path.join(dir_root, 'dic.txt')
#dic_path = os.path.join(sys.path[0], 'dic.txt')
print(dic_path)


def screen_shot():
    with open(dic_path, 'r', encoding='utf-8') as f:
        dic = eval(f.read())
    temp = []
    for i in range(length):
        brand = lis_name[i]
        amount = get_amount(dic_id[brand])
        for key, value in dic[brand].items():
            if amount >= key and value == 0:
                temp.append((brand, key))
                dic[brand][key] = 1
    if temp:
        with open(dic_path, 'w', encoding='utf-8') as f:
            f.write(str(dic))
        binary_pics = []
        # print(f'start {now()}')
        for i in range(6):
            binary_pics.append(browser.get_screenshot_as_png())
        # print(f'end   {now()}')
        for x in temp:
            brand = x[0]
            key = x[1]
            print(f'barnd: {brand} {dic[brand]} {now()}')
            for i in range(6):
                name = f'{key}-{i}.png'
                file_path = os.path.join(dir_root, brand, name)
                with open(file_path, 'wb') as f:
                    f.write(binary_pics[i])


while 1:
    try:
        screen_shot()
    except Exception as e:
        print(e)
        break
