def ups():
    import urllib.request, urllib.error, urllib.parse
    import requests
    from bs4 import BeautifulSoup
    import pymysql
    from  datetime import date
    from requests.exceptions import ReadTimeout, ConnectTimeout, HTTPError, ConnectionError, RequestException
    import time
    import pymongo

    today_str=date.today().strftime('%Y%m%d') # ###新增 获取当天日期，并转成字符串YYYYMMDD的格式
    today_table_name = 'ups'+ today_str # ###新增，表的名称
    client = pymongo.MongoClient('localhost', 27017)  # 连接数据库MDB
    mydb = client['hljcors基准站ups状态数据']  # 新建数据库
    mydb[today_table_name].drop()  # ### 删掉mongo数据库当天的数据表
    ups1 = mydb[today_table_name]  # 新建数据集合(表结构)，以当天日期为表
    #today = datetime.date.today()
    #now_today = ['today']
    #list_today = list(now_today)
    #for t in list_today:
    # 登录的用户名和密码
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='hljcors基准站ups状态数据', port=3306, charset='utf8') # ###数据库的密码改成了我本地数据库的密码，到时候记得改回来
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {today_table_name}")  # 使用 execute() 方法执行 SQL，如果表存在则删除 ### 修改
    sql = f"""CREATE TABLE ups{today_str}(
             ID int(20) not null AUTO_INCREMENT,
             基准站站名  text,
             输入电压 text,
             输出电压 text,
             最大输出电压 text,
             最小输出电压 text,
             频率（赫兹） text,
             总电压 text,
             电池容量 text,
             温度 text,
             运行状态 text,
             primary key(id)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE OK")
    username = "admin"
    password = "admin"

    # url_dq_1="http://10.84.1.2/XML/UPSS.xml"
    def Func(url, username, password):
        try:
            # 创建一个密码管理者
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            # 添加用户名和密码
            password_mgr.add_password(None, url, username, password)
            # 创建了一个新的handler
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            # 创建 "opener"
            opener = urllib.request.build_opener(handler)
            # 使用 opener 获取一个URL
            opener.open(url)
            # 安装 opener.
            urllib.request.install_opener(opener)
            # urllib2.urlopen 使用上面的opener.
            ret = urllib.request.urlopen(url)
            return ret.read()
        except urllib.error.HTTPError as e:
            if e.code == 401:
                return "authorization failed"
            else:
                raise e
        except:
            return None

    list_ups_IP = [  # 拜泉、杜蒙、齐齐哈尔作为备用设备
        # 大庆市    4座基准站
        "http://10.98.168.52/",  # 肇源基准站
        "http://173.18.32.80/",  # 大同基准站
        "http://173.18.32.81/",  # 大庆基准站
        "http://173.18.32.82/",  # 林甸基准站
        # 大兴安岭地区    7座基准站
        "http://10.100.158.52/",  # 加格达奇基准站
        "http://10.100.172.211/",  # 塔河基准站
        "http://10.100.180.52/",  # 北极基准站
        "http://10.92.1.2/",  # 北疆基准站
        "http://10.92.2.2/",  # 白银纳基准站
        "http://10.92.3.2/",  # 盘古基准站
        "http://10.92.4.2/",  # 兴安基准站
        # 哈尔滨市    11座基准站
        "http://10.81.1.2/",  # 东兴基准站
        "http://10.81.2.2/",  # 木兰基准站
        "http://10.81.3.2/",  # 冲河基准站
        "http://10.81.4.2/",  # 亚布力基准站
        "http://10.81.6.2/",  # 凤山基准站
        "http://10.81.9.2/",  # 西集基准站
        "http://10.97.44.52/",  # 五常基准站
        "http://10.97.52.52/",  # 方正基准站
        "http://10.97.56.52/",  # 宾县基准站
        "http://10.97.60.52/",  # 依兰基准站
        "http://172.30.24.131/",  # 哈尔滨基准站
        "http://10.97.36.52/",  # 尚志基准站
        # 鹤岗市    4座基准站
        "http://10.94.1.2/",  # 太平沟基准站
        "http://10.94.2.2/",  # 双丰基准站
        "http://10.94.218.143/",  # 绥滨基准站
        "http://10.99.96.52/",  # 萝北基准站
        # 黑河市   9座基准站
        "http://10.88.1.2/",  # 前进基准站
        "http://10.88.2.2/",  # 宝山基准站
        "http://10.88.3.2/",  # 孙吴基准站
        "http://10.88.4.2/",  # 通北基准站
        "http://10.88.5.2/",  # 塔溪基准站
        "http://10.88.6.2/",  # 龙镇基准站
        "http://10.88.7.2/",  # 七星泡基准站
        "http://10.88.8.2/",  # 吉岭库基准站
        "http://10.99.228.52/",  # 北安基准站
        # 鸡西市   5座基准站
        "http://10.89.1.2/",  # 虎林基准站
        "http://10.89.2.2/",  # 虎头基准站
        "http://10.89.3.2/",  # 东方红基准站
        "http://10.99.36.52/",  # 密山基准站
        "http://172.19.140.216/",  # 鸡西基准站
        # 佳木斯市    12座基准站
        "http://10.84.1.2/",  # 前锋基准站
        "http://10.84.2.2/",  # 别拉洪基准站
        "http://10.84.3.2/",  # 兴隆岗基准站
        "http://10.84.4.2/",  # 创业基准站
        "http://10.84.5.2/",  # 同江基准站
        "http://10.84.6.2/",  # 勤得利基准站
        "http://10.84.7.2/",  # 汤原基准站
        "http://10.84.8.2/",  # 星火基准站
        "http://10.84.9.2/",  # 梨丰基准站
        "http://10.98.100.52/",  # 富锦基准站
        "http://10.98.112.52/",  # 桦南基准站
        "http://172.19.140.216/",  # 鸡西基准站
        # 牡丹江市    10座基准站
        "http://10.83.1.2/",  # 共和基准站
        "http://10.83.2.2/",  # 东宁基准站
        "http://10.83.3.2/",  # 雪乡基准站
        "http://10.83.4.2/",  # 老黑山基准站
        "http://10.83.5.2/",  # 西岗基准站
        "http://10.83.6.2/",  # 海林基准站
        "http://10.83.7.2/",  # 二道河基准站
        "http://10.83.8.2/",  # 镜湖基准站
        "http://10.98.44.52/",  # 穆棱基准站
        "http://10.98.48.192/",  # 团结基准站
        # 七台河市  3座基准站
        "http://10.100.224.52/",  # 勃利基准站
        "http://10.91.1.2/",  # 七台河基准站
        "http://10.91.2.4/",  # 宏伟基准站
        # 齐齐哈尔市   8座基准站
        "http://10.82.1.2/",  # 富裕基准站
        "http://10.82.2.2/",  # 克山基准站
        "http://10.82.3.2/",  # 大兴基准站
        "http://10.82.4.2/",  # 碾子山基准站
        "http://10.82.5.2/",  # 依龙基准站
        "http://10.82.6.2/",  # 龙河基准站
        "http://10.97.172.52/",  # 依安基准站
        "http://10.97.188.52/",  # 龙江基准站
        "http://10.87.180.52/",  # 泰来基准站
        # 双鸭山市  6座基准站
        "http://10.90.1.2/",  # 小佳河基准站
        "http://10.90.2.2/",  # 红旗岭基准站
        "http://10.99.164.52/",  # 宝清基准站
        "http://10.99.168.52/",  # 饶河基准站
        "http://10.99.172.52/",  # 友谊基准站
        "http://172.19.130.52/",  # 双鸭山基准站
        # 绥化市  8座基准站
        "http://10.81.5.8/",  # 庆阳基准站
        "http://10.81.8.2/",  # 四站基准站
        "http://10.86.1.2/",  # 庆安基准站
        "http://10.86.2.2/",  # 四海店基准站
        "http://10.86.3.2/",  # 明水基准站
        "http://10.86.4.2/",  # 青冈基准站
        "http://10.86.5.2/",  # 厢白基准站
        "http://10.94.216.228/",  # 安民基准站
        # 伊春市   7座基准站
        "http://10.87.1.2/",  # 金山屯基准站
        "http://10.87.2.2/",  # 乌云基准站
        "http://10.87.3.2/",  # 铁力基准站
        "http://10.87.4.2/",  # 朗乡基准站
        "http://10.98.222.53/",  # 伊春基准站
        "http://10.98.224.52/",  # 五营基准站
        # "http://10.98.228.52/" ,  # 乌伊岭基准站
        # 气象局需核实  4座基准站
        "http://10.97.168.52/",  # 甘南基准站
        "http://10.99.224.52/",  # 黑河基准站
        "http://10.100.168.52/",  # 新林基准站
        "http://10.100.160.53/"  # 呼玛基准站
    ]
    dist_ups_IP = {
        # 大庆市
        "http://10.98.168.52/": "肇源基准站",
        "http://173.18.32.80/": "大同基准站",
        "http://173.18.32.81/": "大庆基准站",
        "http://173.18.32.82/": "林甸基准站",
        # 大兴安岭地区
        "http://10.100.158.52/": "加格达奇基准站",
        "http://10.100.172.211/": "塔河基准站",
        "http://10.100.180.52/": "北极基准站",
        "http://10.92.1.2/": "北疆基准站",
        "http://10.92.2.2/": "白银纳基准站",
        "http://10.92.3.2/": "盘古基准站",
        "http://10.92.4.2/": "兴安基准站",
        # 哈尔滨市
        "http://10.81.1.2/": "东兴基准站",
        "http://10.81.2.2/": "木兰基准站",
        "http://10.81.3.2/": "冲河基准站",
        "http://10.81.4.2/": "亚布力基准站",
        "http://10.81.6.2/": "凤山基准站",
        "http://10.81.9.2/": "西集基准站",
        "http://10.97.44.52/": "五常基准站",
        "http://10.97.52.52/": "方正基准站",
        "http://10.97.56.52/": "宾县基准站",
        "http://10.97.60.52/": "依兰基准站",
        "http://172.30.24.131/": "哈尔滨基准站",
        "http://10.97.76.50/": "延寿基准站",
        "http://10.97.36.52/": "尚志基准站",
        # 鹤岗市
        "http://10.94.1.2/": "太平沟基准站",
        "http://10.94.2.2/": "双丰基准站",
        "http://10.94.218.143/": "绥滨基准站",
        "http://10.99.96.52/": "萝北基准站",
        # 黑河市
        "http://10.88.1.2/": "前进基准站",
        "http://10.88.2.2/": "宝山基准站",
        "http://10.88.3.2/": "孙吴基准站",
        "http://10.88.4.2/": "通北基准站",
        "http://10.88.5.2/": "塔溪基准站",
        "http://10.88.6.2/": "龙镇基准站",
        "http://10.88.7.2/": "七星泡基准站",
        "http://10.88.8.2/": "吉岭库基准站",
        "http://10.99.228.52/": "北安基准站",
        # 鸡西市
        "http://10.89.1.2/": "虎林基准站",
        "http://10.89.2.2/": "虎头基准站",
        "http://10.89.3.2/": "东方红基准站",
        "http://10.99.36.52/": "密山基准站",
        "http://172.19.140.216/": "鸡西基准站",
        # 佳木斯市
        "http://10.84.1.2/": "前锋基准站",
        "http://10.84.2.2/": "别拉洪基准站",
        "http://10.84.3.2/": "兴隆岗基准站",
        "http://10.84.4.2/": "创业基准站",
        "http://10.84.5.2/": "同江基准站",
        "http://10.84.6.2/": "勤得利基准站",
        "http://10.84.7.2/": "汤原基准站",
        "http://10.84.8.2/": "星火基准站",
        "http://10.84.9.2/": "梨丰基准站",
        "http://10.98.100.52/": "富锦基准站",
        "http://10.98.112.52/": "桦南基准站",
        "http://172.19.140.216/": "鸡西基准站",
        # 牡丹江市
        "http://10.83.1.2/": "共和基准站",
        "http://10.83.2.2/": "东宁基准站",
        "http://10.83.3.2/": "雪乡基准站",
        "http://10.83.4.2/": "老黑山基准站",
        "http://10.83.5.2/": "西岗基准站",
        "http://10.83.6.2/": "海林基准站",
        "http://10.83.7.2/": "二道河基准站",
        "http://10.83.8.2/": "镜湖基准站",
        "http://10.98.44.52/": "穆棱基准站",
        "http://10.98.48.192/": "团结基准站",
        # 七台河市
        "http://10.100.224.52/": "勃利基准站",
        "http://10.91.1.2/": "七台河基准站",
        "http://10.91.2.4/": "宏伟基准站",
        # 齐齐哈尔市
        "http://10.82.1.2/": "富裕基准站",
        "http://10.82.2.2/": "克山基准站",
        "http://10.82.3.2/": "大兴基准站",
        "http://10.82.4.2/": "碾子山基准站",
        "http://10.82.5.2/": "依龙基准站",
        "http://10.82.6.2/": "龙河基准站",
        "http://10.97.172.52/": "依安基准站",
        "http://10.97.188.52/": "龙江基准站",
        "http://10.87.180.52/": "泰来基准站",
        # 双鸭山市
        "http://10.90.1.2/": "小佳河基准站",
        "http://10.90.2.2/": "红旗岭基准站",
        "http://10.99.164.52/": "宝清基准站",
        "http://10.99.168.52/": "饶河基准站",
        "http://10.99.172.52/": "友谊基准站",
        "http://172.19.130.52/": "双鸭山基准站",
        # 绥化市
        "http://10.81.5.8/": "庆阳基准站",
        "http://10.81.8.2/": "四站基准站",
        "http://10.86.1.2/": "庆安基准站",
        "http://10.86.2.2/": "四海店基准站",
        "http://10.86.3.2/": "明水基准站",
        "http://10.86.4.2/": "青冈基准站",
        "http://10.86.5.2/": "厢白基准站",
        "http://10.94.216.228/": "安民基准站",
        # 伊春市
        "http://10.87.1.2/": "金山屯基准站",
        "http://10.87.2.2/": "乌云基准站",
        "http://10.87.3.2/": "铁力基准站",
        "http://10.87.4.2/": "朗乡基准站",
        "http://10.98.222.53/": "伊春基准站",
        "http://10.98.224.52/": "五营基准站",
        # "http://10.98.228.52/":"乌伊岭基准站",  基准站内作为备用设备
        # 气象局需核实
        "http://10.97.168.52/": "甘南基准站",
        "http://10.99.224.52/": "黑河基准站",
        "http://10.100.168.52/": "新林基准站",
        "http://10.100.160.53/": "呼玛基准站"
    }
    for ups_IP in list_ups_IP:
        try:
            print(ups_IP)
            str_ups = 'XML/UPSS.xml'
            url_ups = ups_IP + str_ups
            # print(url_ups)
            ups_url = requests.get(url_ups, timeout=10)
            # ups_url = requests.get(ups_url,timeout = 20)
            # ups_url.encoding = 'utf-8'
            res_ups = Func(url_ups, username, password)  # 输入账号、密码登录网页进行爬取
            # print(res_ups)
            soup_ups = BeautifulSoup(res_ups, 'html.parser')
            # print(soup_ups)
            xx_name_ld = str(soup_ups.text)  # 转为文本
            # print(xx_name_ld)
            list_ups = xx_name_ld.split('[#|]')  # 建列表
            print(list_ups)
            # print(list1)
            # print(list1[0])
            list_ups_srdy = float(list_ups[0])  # 输入电压
            list_ups_scdy = float(list_ups[1])  # 输出电压
            list_ups_maxscdy = float(list_ups[2])  # 最大输出电压
            list_ups_minscdy = float(list_ups[3])  # 最小输出电压
            list_ups_pv = float(list_ups[5])  # 频率
            list_ups_zdy = float(list_ups[6])  # 总电压
            list_ups_dcrl = float(list_ups[9])  # 电池容量
            list_ups_wd = float(list_ups[7])  # 温度
            jzzmc_ups = dist_ups_IP[ups_IP]  # 从字典中获取基准站名称
            # print(ups_IP,jzzmc_ups,xx_ups_ds)
            time.sleep(1)
            ups1.insert_one({
                '基准站站名': jzzmc_ups, '输入电压': list_ups_srdy, '输出电压': list_ups_scdy,
                '最大输出电压': list_ups_maxscdy, '最小输出电压': list_ups_minscdy, '频率（赫兹）': list_ups_pv, '总电压': list_ups_zdy,
                '电池容量': list_ups_dcrl, '温度': list_ups_wd, '运行状态': '运行正常'
            })
            cursor.execute(
                f"insert into {today_table_name} (基准站站名,输入电压,输出电压,最大输出电压,最小输出电压,频率（赫兹）,总电压,电池容量,温度,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (jzzmc_ups, list_ups_srdy, list_ups_scdy, list_ups_maxscdy, list_ups_minscdy, list_ups_pv, list_ups_zdy,
                 list_ups_dcrl, list_ups_wd, "运行正常"))
            conn.commit()
        except ReadTimeout as e:
            print('请求超时:', ups_IP)  # 网络延时率的测试
            jzzmc_ups = dist_ups_IP[ups_IP]  # 从字典中获取基准站名称
            ups1.insert_one({
                '基准站站名': jzzmc_ups, '输入电压': 'NULL', '输出电压': 'NULL',
                '最大输出电压': 'NULL', '最小输出电压': 'NULL', '频率（赫兹）': 'NULL', '总电压': 'NULL', '电池容量': 'NULL', '温度': 'NULL',
                '运行状态': '请求超时'
            })
            cursor.execute(
                f"insert into {today_table_name} (基准站站名,输入电压,输出电压,最大输出电压,最小输出电压,频率（赫兹）,总电压,电池容量,温度,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (jzzmc_ups, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "请求超时"))
            conn.commit()
        except ConnectionError as e:
            print('网络连接异常:', ups_IP)  # 网络出现故障，连接异常
            jzzmc_ups = dist_ups_IP[ups_IP]  # 从字典中获取基准站名称
            ups1.insert_one({
                '基准站站名': jzzmc_ups, '输入电压': 'NULL', '输出电压': 'NULL',
                '最大输出电压': 'NULL', '最小输出电压': 'NULL', '频率（赫兹）': 'NULL', '总电压': 'NULL', '电池容量': 'NULL', '温度': 'NULL',
                '运行状态': '网络连接异常'
            })
            cursor.execute(
                f"insert into {today_table_name} (基准站站名,输入电压,输出电压,最大输出电压,最小输出电压,频率（赫兹）,总电压,电池容量,温度,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (jzzmc_ups, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "网络连接异常"))
            conn.commit()
        except RequestException as e:
            print('请求失败:', ups_IP)
            jzzmc_ups = dist_ups_IP[ups_IP]  # 从字典中获取基准站名称
            ups1.insert_one({
                '基准站站名': jzzmc_ups, '输入电压': 'NULL', '输出电压': 'NULL',
                '最大输出电压': 'NULL', '最小输出电压': 'NULL', '频率（赫兹）': 'NULL', '总电压': 'NULL', '电池容量': 'NULL', '温度': 'NULL',
                '运行状态': '请求失败'
            })
            cursor.execute(
                f"insert into {today_table_name} (基准站站名,输入电压,输出电压,最大输出电压,最小输出电压,频率（赫兹）,总电压,电池容量,温度,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (jzzmc_ups, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "请求失败"))
            conn.commit()


