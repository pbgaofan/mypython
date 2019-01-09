def receiver():
    import requests
    from bs4 import BeautifulSoup
    from lxml import etree
    from urllib.request import urlopen
    from requests.exceptions import ReadTimeout, ConnectTimeout, HTTPError, ConnectionError, RequestException
    import time
    import pymongo
    import urllib.request, urllib.error, urllib.parse
    from datetime import date
    import datetime
    import pymysql
    import csv
    import codecs
    import warnings

    
    client = pymongo.MongoClient('localhost', 27017)  # 连接数据库MDB
    #today = datetime.date.today()
    #now_today = ['today']
    #list_today = list(now_today)
    mydb = client['hljcors基准站接收机状态数据']  # 新建数据库
    today_str = date.today().strftime('%Y%m%d')
    today_table_name = 'jsj'+today_str
    mydb[today_table_name].drop()  # ### mongo数据库中如果有名为today_table_name的表，则删掉
    jsj = mydb[today_table_name]  # 新建数据集合(表结构)
    conn = pymysql.connect(host='localhost', user='root', passwd='root', db='hljcors基准站接收机状态数据', port=3306, charset='utf8')
    cursor = conn.cursor()
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        cursor.execute(f"DROP TABLE IF EXISTS {today_table_name}")  # 使用 execute() 方法执行 SQL，如果表存在则删除
    # 使用预处理语句创建表
    sql = f"""CREATE TABLE {today_table_name}(
             ID int(20) not null AUTO_INCREMENT,
             基准站站名  text,
             地市  text,
             基准站IP text,
             基准站名称 text,
             运行时长 text,
             纬度（度） text,
             经度（度） text,
             高度（米） text,
             跟踪到的卫星数（颗） text,
             接收机SN号 text,
             天线盘SN号 text,
             天线类型 text,
             天线高（米） text,
             磁盘剩余空间（兆） text,
             磁盘总空间（兆） text,
             温度（°C） text,
             剩余电量 text,
             以太网MAC地址 text,
             蓝牙MAC地址  text,
             固件版本 text,
             启动版本 text,
             天线数据库版本 text,
             硬件版本 text,
             输出 text,
             运行状态 text,
             primary key(id)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE OK")
    #for t in list_today:
        #print(2, today)
    list_IP = [
        # 新建基准站、气象局利用站（除金山屯、七星泡、吉岭库、勃利基准站）  代码里共包括113座基准站(新建站100座，气象局利用站4座，利用国家站9座)，目前玉泉基准站无网络通讯设备，无法获取信息。大庆基准站因网页验证，暂未获取。
        # 哈尔滨市14座基准站
        "http://10.81.1.1/", "http://10.81.2.1/",
        "http://10.81.3.1/", "http://10.81.4.1/",
        "http://10.81.5.1/", "http://10.81.6.1/",
        "http://10.81.9.1/", "http://10.97.56.51/",
        "http://10.97.52.51/", "http://10.97.36.51/",
        "http://10.97.40.51/", "http://10.97.44.51/",
        "http://10.97.76.53/", "http://10.97.60.51/",
        # 齐齐哈尔市12座基准站(含气象局利用站2座齐齐哈尔、泰来站)
        "http://10.82.1.1/", "http://10.82.2.1/",
        "http://10.82.3.1/", "http://10.82.4.1/",
        "http://10.82.5.1/", "http://10.82.6.1/",
        "http://10.97.192.51/", "http://10.97.168.51/",
        "http://10.97.188.53/", "http://10.97.172.51/",
        "http://10.97.158.51/", "http://10.97.180.51/",
        # 牡丹江市10座基准站
        "http://10.83.1.1/", "http://10.83.2.1/",
        "http://10.83.3.1/", "http://10.83.4.1/",
        "http://10.83.5.1/", "http://10.83.6.1/",
        "http://10.83.7.1/", "http://10.83.8.1/",
        "http://10.98.44.51/", "http://10.98.48.191/",
        # 佳木斯市11座基准站
        "http://10.84.1.1/", "http://10.84.2.1/",
        "http://10.84.3.1/", "http://10.84.4.1/",
        "http://10.84.5.1/", "http://10.84.6.1/",
        "http://10.84.7.1/", "http://10.84.8.1/",
        "http://10.84.9.1/", "http://10.98.112.51/",
        "http://10.98.100.51/",
        # 大庆市2座基准站
        "http://10.98.172.52/", "http://10.98.168.51/",
        # 绥化市9座基准站
        "http://10.86.1.1/", "http://10.86.2.1/",
        "http://10.86.3.1/", "http://10.86.4.1/",
        "http://10.86.5.1/", "http://10.81.8.1/",
        "http://10.94.216.228:8080/", "http://10.100.32.51/",
        "http://10.100.52.51/",
        # 伊春市7座基准站
        "http://10.87.1.1/", "http://10.87.2.1/",
        "http://10.87.3.1/", "http://10.87.4.1/",
        "http://10.98.222.51/", "http://10.98.228.51/",  # "http://10.87.1.1/",
        "http://10.98.224.53/",
        # 鹤岗市4座基准站
        "http://10.94.1.1/", "http://10.94.2.1/",
        "http://10.94.218.143:8080/", "http://10.99.96.51/",
        # 黑河市11座基准站(含气象局利用站1座黑河站)
        "http://10.88.1.1/", "http://10.88.2.1/",
        "http://10.88.3.1/", "http://10.88.4.1/",
        "http://10.88.5.1/", "http://10.88.6.1/",
        "http://10.88.7.1/", "http://10.88.8.1/",
        "http://10.99.228.51/", "http://10.99.236.51/",  # "http://10.88.7.1/"  "http://10.88.8.1/",
        "http://10.99.224.51/",
        # 鸡西市5站
        "http://10.89.1.1/", "http://10.89.2.1/",
        "http://10.89.3.1/", "http://172.19.140.213/",
        "http://10.99.36.51/",
        # 双鸭山市6站
        "http://10.90.1.1/", "http://10.90.2.1/",
        "http://10.99.168.51/", "http://172.19.130.51/",
        "http://10.99.172.51/", "http://10.99.164.51/",
        # 七台河市3站
        "http://10.91.1.1/", "http://10.91.2.1/",
        "http://10.100.224.51/",  # "http://10.100.224.51/",
        # 大兴安岭地区10站(含气象局利用站1座塔河站)
        "http://10.92.1.1/", "http://10.92.2.1/",
        "http://10.92.3.1/", "http://10.92.4.1/",
        "http://10.100.180.51/", "http://10.100.160.51/",
        "http://10.100.164.51/", "http://10.100.158.51/",
        "http://10.100.168.51/", "http://10.100.172.51/",
        # 国家站9座基准站
        "http://172.30.24.17/", "http://172.30.24.33/",
        "http://172.30.24.49/", "http://172.30.24.81/",
        "http://172.30.24.97/", "http://172.30.24.113/",
        "http://172.30.24.65/"  # "http://172.30.24.1/", ,"http://172.30.24.129/"
    ]
    dict_zm = {  # 新建基准站、气象局利用站（除金山屯、七星泡、吉岭库、勃利基准站） 根据字典导出基准站站名
        # 哈尔滨市14座基准站
        "http://10.81.1.1/": "东兴基准站", "http://10.81.2.1/": "木兰基准站",
        "http://10.81.3.1/": "冲河基准站", "http://10.81.4.1/": "亚布力基准站",
        "http://10.81.5.1/": "庆阳基准站", "http://10.81.6.1/": "凤山基准站",
        "http://10.81.9.1/": "西集基准站", "http://10.97.56.51/": "宾县基准站",
        "http://10.97.52.51/": "方正基准站", "http://10.97.36.51/": "尚志基准站",
        "http://10.97.40.51/": "双城基准站", "http://10.97.44.51/": "五常基准站",
        "http://10.97.76.53/": "延寿基准站", "http://10.97.60.51/": "依兰基准站",
        # 齐齐哈尔市12座基准站(含气象局利用站2座齐齐哈尔、泰来站)
        "http://10.82.1.1/": "富裕基准站", "http://10.82.2.1/": "克山基准站",
        "http://10.82.3.1/": "大兴基准站", "http://10.82.4.1/": "碾子山基准站",
        "http://10.82.5.1/": "依龙基准站", "http://10.82.6.1/": "龙河基准站",
        "http://10.97.192.51/": "拜泉基准站", "http://10.97.168.51/": "甘南基准站",
        "http://10.97.188.53/": "龙江基准站", "http://10.97.172.51/": "依安基准站",
        "http://10.97.158.51/": "齐齐哈尔基准站", "http://10.97.180.51/": "泰来基准站",
        # 牡丹江市10座基准站
        "http://10.83.1.1/": "共和基准站", "http://10.83.2.1/": "东宁基准站",
        "http://10.83.3.1/": "雪乡基准站", "http://10.83.4.1/": "老黑山基准站",
        "http://10.83.5.1/": "西岗基准站", "http://10.83.6.1/": "海林基准站",
        "http://10.83.7.1/": "二道河基准站", "http://10.83.8.1/": "镜湖基准站",
        "http://10.98.44.51/": "穆棱基准站", "http://10.98.48.191/": "团结基准站",
        # 佳木斯市11座基准站
        "http://10.84.1.1/": "前锋基准站", "http://10.84.2.1/": "别拉洪基准站",
        "http://10.84.3.1/": "兴隆岗基准站", "http://10.84.4.1/": "创业基准站",
        "http://10.84.5.1/": "同江基准站", "http://10.84.6.1/": "勤得利基准站",
        "http://10.84.7.1/": "汤原基准站", "http://10.84.8.1/": "星火基准站",
        "http://10.84.9.1/": "梨丰基准站", "http://10.98.112.51/": "桦南基准站",
        "http://10.98.100.51/": "富锦基准站",
        # 大庆市2座基准站
        "http://10.98.172.52/": "杜蒙基准站", "http://10.98.168.51/": "肇源基准站",
        # 绥化市9座基准站
        "http://10.86.1.1/": "庆安基准站", "http://10.86.2.1/": "四海店基准站",
        "http://10.86.3.1/": "明水基准站", "http://10.86.4.1/": "青冈基准站",
        "http://10.86.5.1/": "厢白基准站", "http://10.81.8.1/": "四站基准站",
        "http://10.94.216.228:8080/": "安民基准站", "http://10.100.32.51/": "绥化基准站",
        "http://10.100.52.51/": "兰西基准站",
        # 伊春市7座基准站
        "http://10.87.1.1/": "金山屯基准站", "http://10.87.2.1/": "乌云基准站",
        "http://10.87.3.1/": "铁力基准站", "http://10.87.4.1/": "朗乡基准站",
        "http://10.98.222.51/": "伊春基准站", "http://10.98.228.51/": "乌伊岭基准站",  # "http://10.87.1.1/":"金山屯"
        "http://10.98.224.53/": "五营基准站",
        # 鹤岗市4座基准站
        "http://10.94.1.1/": "太平沟基准站", "http://10.94.2.1/": "双丰基准站",
        "http://10.94.218.143:8080/": "绥滨基准站", "http://10.99.96.51/": "萝北基准站",
        # 黑河市11座基准站(含气象局利用站1座黑河站)
        "http://10.88.1.1/": "前进基准站", "http://10.88.2.1/": "宝山基准站",
        "http://10.88.3.1/": "孙吴基准站", "http://10.88.4.1/": "通北基准站",
        "http://10.88.5.1/": "塔溪基准站", "http://10.88.6.1/": "龙镇基准站",
        "http://10.88.7.1/": "七星泡基准站", "http://10.88.8.1/": "吉岭库基准站",
        "http://10.99.228.51/": "北安基准站", "http://10.99.236.51/": "逊克基准站",
        # "http://10.88.7.1/":"七星泡基准站"    "http://10.88.8.1/":"吉岭库基准站",
        "http://10.99.224.51/": "黑河基准站",
        # 鸡西市5座基准站
        "http://10.89.1.1/": "虎林基准站", "http://10.89.2.1/": "虎头基准站",
        "http://10.89.3.1/": "东方红基准站", "http://172.19.140.213/": "鸡西基准站",
        "http://10.99.36.51/": "密山基准站",
        # 双鸭山市6座基准站
        "http://10.90.1.1/": "小佳河基准站", "http://10.90.2.1/": "红旗岭基准站",
        "http://10.99.168.51/": "饶河基准站", "http://172.19.130.51/": "双鸭山基准站",
        "http://10.99.172.51/": "友谊基准站", "http://10.99.164.51/": "宝清基准站",
        # 七台河市3座基准站
        "http://10.91.1.1/": "七台河基准站", "http://10.91.2.1/": "宏伟基准站",
        "http://10.100.224.51/": "勃利基准站",  # "http://10.100.224.51/":"勃利基准站",
        # 大兴安岭地区10座基准站(含气象局利用站1座塔河站)
        "http://10.92.1.1/": "北疆基准站", "http://10.92.2.1/": "白银纳基准站",
        "http://10.92.3.1/": "盘古基准站", "http://10.92.4.1/": "兴安基准站",
        "http://10.100.180.51/": "北极基准站", "http://10.100.160.51/": "呼玛基准站",
        "http://10.100.164.51/": "呼中基准站", "http://10.100.158.51/": "加格达奇基准站",
        "http://10.100.168.51/": "新林基准站", "http://10.100.172.51/": "塔河基准站",
        # 国家站9座基准站
        "http://172.30.24.17/": "嘉荫基准站", "http://172.30.24.33/": "讷河基准站",
        "http://172.30.24.49/": "宁安基准站", "http://172.30.24.81/": "林口基准站",
        "http://172.30.24.97/": "杜尔伯特基准站", "http://172.30.24.113/": "嫩江基准站",
        "http://172.30.24.65/": "兴凯湖基准站"  # "http://172.30.24.1/":"海伦基准站", "http://172.30.24.129/":"哈尔滨基准站"
    }
    dict_ds = {  # 新建基准站、气象局利用站（除金山屯、七星泡、吉岭库、勃利基准站） 根据字典导出基准站所属地市
        # 哈尔滨市14座基准站
        "东兴基准站": "哈尔滨市", "木兰基准站": "哈尔滨市",
        "冲河基准站": "哈尔滨市", "亚布力基准站": "哈尔滨市",
        "庆阳基准站": "哈尔滨市", "凤山基准站": "哈尔滨市",
        "西集基准站": "哈尔滨市", "宾县基准站": "哈尔滨市",
        "方正基准站": "哈尔滨市", "尚志基准站": "哈尔滨市",
        "双城基准站": "哈尔滨市", "五常基准站": "哈尔滨市",
        "延寿基准站": "哈尔滨市", "依兰基准站": "哈尔滨市",
        # 齐齐哈尔市12座基准站(含气象局利用站2座齐齐哈尔、泰来站)
        "富裕基准站": "齐齐哈尔市", "克山基准站": "齐齐哈尔市",
        "大兴基准站": "齐齐哈尔市", "碾子山基准站": "齐齐哈尔市",
        "依龙基准站": "齐齐哈尔市", "龙河基准站": "齐齐哈尔市",
        "拜泉基准站": "齐齐哈尔市", "甘南基准站": "齐齐哈尔市",
        "龙江基准站": "齐齐哈尔市", "依安基准站": "齐齐哈尔市",
        "齐齐哈尔基准站": "齐齐哈尔市", "泰来基准站": "齐齐哈尔市",
        # 牡丹江市10座基准站
        "共和基准站": "牡丹江市", "东宁基准站": "牡丹江市",
        "雪乡基准站": "牡丹江市", "老黑山基准站": "牡丹江市",
        "西岗基准站": "牡丹江市", "海林基准站": "牡丹江市",
        "二道河基准站": "牡丹江市", "镜湖基准站": "牡丹江市",
        "穆棱基准站": "牡丹江市", "团结基准站": "牡丹江市",
        # 佳木斯市11座基准站
        "前锋基准站": "佳木斯市", "别拉洪基准站": "佳木斯市",
        "兴隆岗基准站": "佳木斯市", "创业基准站": "佳木斯市",
        "同江基准站": "佳木斯市", "勤得利基准站": "佳木斯市",
        "汤原基准站": "佳木斯市", "星火基准站": "佳木斯市",
        "梨丰基准站": "佳木斯市", "桦南基准站": "佳木斯市",
        "富锦基准站": "佳木斯市",
        # 大庆市2座基准站
        "杜蒙基准站": "大庆市", "肇源基准站": "大庆市",
        # 绥化市9座基准站
        "庆安基准站": "绥化市", "四海店基准站": "绥化市",
        "明水基准站": "绥化市", "青冈基准站": "绥化市",
        "厢白基准站": "绥化市", "四站基准站": "绥化市",
        "安民基准站": "绥化市", "绥化基准站": "绥化市",
        "兰西基准站": "绥化市",
        # 伊春市7座基准站
        "金山屯基准站": "伊春市", "乌云基准站": "伊春市",
        "铁力基准站": "伊春市", "朗乡基准站": "伊春市",
        "伊春基准站": "伊春市", "乌伊岭基准站": "伊春市",  # "金山屯基准站":"伊春市"
        "五营基准站": "伊春市",
        # 鹤岗市4座基准站
        "太平沟基准站": "鹤岗市", "双丰基准站": "鹤岗市",
        "绥滨基准站": "鹤岗市", "萝北基准站": "鹤岗市",
        # 黑河市11座基准站(含气象局利用站1座黑河站)
        "前进基准站": "黑河市", "宝山基准站": "黑河市",
        "孙吴基准站": "黑河市", "通北基准站": "黑河市",
        "塔溪基准站": "黑河市", "龙镇基准站": "黑河市",
        "七星泡基准站": "黑河市", "吉岭库基准站": "黑河市",
        "北安基准站": "黑河市", "逊克基准站": "黑河市",  # "七星泡基准站":"黑河市"    "吉岭库基准站":"黑河市",
        "黑河基准站": "黑河市",
        # 鸡西市5座基准站
        "虎林基准站": "鸡西市", "虎头基准站": "鸡西市",
        "东方红基准站": "鸡西市", "鸡西基准站": "鸡西市",
        "密山基准站": "鸡西市",
        # 双鸭山市6座基准站
        "小佳河基准站": "双鸭山市", "红旗岭基准站": "双鸭山市",
        "饶河基准站": "双鸭山市", "双鸭山基准站": "双鸭山市",
        "友谊基准站": "双鸭山市", "宝清基准站": "双鸭山市",
        # 七台河市3座基准站
        "七台河基准站": "七台河市", "宏伟基准站": "七台河市",
        "勃利基准站": "七台河市",  # "勃利基准站":"七台河市",
        # 大兴安岭地区10座基准站(含气象局利用站1座塔河站)
        "北疆基准站": "大兴安岭地区", "白银纳基准站": "大兴安岭地区",
        "盘古基准站": "大兴安岭地区", "兴安基准站": "大兴安岭地区",
        "北极基准站": "大兴安岭地区", "呼玛基准站": "大兴安岭地区",
        "呼中基准站": "大兴安岭地区", "加格达奇基准站": "大兴安岭地区",
        "新林基准站": "大兴安岭地区", "塔河基准站": "大兴安岭地区",
        # 国家站9座基准站
        "嘉荫基准站": "伊春市", "讷河基准站": "齐齐哈尔市",
        "宁安基准站": "牡丹江市", "林口基准站": "牡丹江市",
        "杜尔伯特基准站": "大庆市", "嫩江基准站": "黑河市",
        "兴凯湖基准站": "鸡西市"  # "海伦基准站":"绥化市","哈尔滨基准站":"哈尔滨市"
    }
    for i in list_IP:
        jzzmc = dict_zm[i]  # 从字典中获取基准站名称
        xx_ds = dict_ds[jzzmc]  # 从字典中获取基准站所在地
        try:
            str_1 = 'xml/dynamic/merge.xml?svData=&dataLogger=&ioConfigData=&powerData=&connStatus='
            str_2 = 'xml/dynamic/merge.xml?sysData=&options='
            str_5 = 'xml/dynamic/merge.xml?ioConfigData=&configData='
            url_1 = i + str_1
            url_2 = i + str_2
            url_5 = i + str_5
            # # 用于pycharm查看用
            res1 = requests.get(url_1, timeout=20)
            res2 = requests.get(url_2, timeout=20)
            res1.encoding = 'utf-8'
            res2.encoding = 'utf-8'
            soup_1 = BeautifulSoup(res1.text, 'html.parser')
            soup_2 = BeautifulSoup(res2.text, 'html.parser')
            cachedir = str(soup_2.select('cachedir')[0].text)
            # print(cachedir)
            str_3_jc = '/xml/dynamic/posData.xml'
            str_4_jc = '/xml/dynamic/merge.xml?&options=&configData='
            str_3 = cachedir + str_3_jc
            str_4 = cachedir + str_4_jc
            url_3 = i + str_3
            url_4 = i + str_4
            # print(url_1)
            # print(url_2)
            # print(url_3)
            # print(url_4)
            # print(url_5)
            res3 = requests.get(url_3, timeout=20)
            res4 = requests.get(url_4, timeout=20)
            res5 = requests.get(url_5, timeout=20)
            res3.encoding = 'utf-8'
            res4.encoding = 'utf-8'
            res5.encoding = 'utf-8'
            soup_3 = BeautifulSoup(res3.text, 'html.parser')
            soup_4 = BeautifulSoup(res4.text, 'html.parser')
            soup_5 = BeautifulSoup(res5.text, 'html.parser')
            # print(soup_3)
            soup_1_space = int(soup_1.select('available')[0].text)
            soup_1_space = (soup_1_space / (1024 * 1024))
            soup_3_time_day = int(soup_3.select('avgtimedays')[0].text)
            soup_3_time_hour = int(soup_3.select('avgtimehr')[0].text)
            soup_3_time_min = int(soup_3.select('avgtimemins')[0].text)
            soup_3_time_second = int(soup_3.select('avgtimesecs')[0].text)
            list_SC = soup_5.select('stream')
            xx_name = str(soup_2.select('ownerstring1')[0].text)  # 提取基准站名称
            xx_time_day = str(soup_3_time_day) + '日'
            xx_time_hour = str(soup_3_time_hour) + '时'
            xx_time_min = str(soup_3_time_min) + '分'
            xx_time_second = str(soup_3_time_second) + '秒'
            xx_time = xx_time_day + xx_time_hour + xx_time_min + xx_time_second  # 计算基准站运行时长，并提取
            xx_avglat = float(soup_3.select('avglat')[0].text)  # 提取基准站纬度
            xx_avglon = float(soup_3.select('avglon')[0].text)  # 提取基准站经度
            xx_avght = str(soup_3.select('avght')[0].text)  # 提取基准站高度
            xx_numfixsvs = str(soup_3.select('numfixsvs')[0].text)  # 提取基准站跟踪的卫星数
            xx_serial = str(soup_2.select('serial')[0].text)  # 提取接收机SN号
            xx_antennaserial = str(soup_4.select('antennaserial')[0].text)  # 提取天线盘SN号
            xx_antennatype = str(soup_4.select('antennatype')[0].text)  # 提取天线类型
            xx_antennaheight = str(soup_4.select('antennaheight')[0].text)  # 提取天线高
            xx_surplusspace = int(soup_1_space)  # 提取磁盘剩余空间
            xx_totalspace = int(soup_2.select('datalogmemlimitmb')[0].text)  # 提取磁盘总空间
            xx_celsius = float(soup_1.select('celsius')[0].text)  # 提取接收机温度
            xx_capacity = float(soup_1.select('capacity')[0].text)  # 提取接收机剩余电量
            xx_mac = str(soup_2.select('mac')[0].text)  # 提取接收机以太网MAC地址
            xx_btaddr = str(soup_2.select('btaddr')[0].text)  # 提取接收机Bluetooth MAC地址
            xx_fwversion = float(soup_2.select('fwversion')[0].text)  # 提取接收机固件版本
            xx_monversion = float(soup_2.select('monversion')[0].text)  # 提取接收机启动版本
            xx_antennaini = float(soup_2.select('antennaini')[0].text)  # 提取接收机天线数据库版本
            xx_hwversion = float(soup_2.select('hwversion')[0].text)  # 提取接收机硬件版本
            list_dksc = []  # 新建接收机端口输出列表
            for j in range(len(list_SC)):
                try:
                    # print('输出：',list_SC[j].select('type')[0].text,'(',list_SC[j].select('port')[0].text,')','-',list_SC[j].select('output')[0].text)
                    xx_dksc_type = str(list_SC[j].select('type')[0].text)
                    xx_dksc_port = str(list_SC[j].select('port')[0].text)
                    xx_dksc_output = str(list_SC[j].select('output')[0].text)
                    xx_dksc = xx_dksc_type + '(' + xx_dksc_port + ')' + '-' + xx_dksc_output
                    xx_list_dksc = list_dksc.append(xx_dksc)
                except:
                    pass
            xx_dksc_join = ';'.join(list_dksc)  # 将列表中的信息进行合并处理
            # jzzmc = dict_zm[i]  # 从字典中获取基准站名称
            # xx_ds = dict_ds[jzzmc]  # 从字典中获取基准站所在地
            # print(i,jzzmc,xx_ds)
            time.sleep(1)
            jsj.insert_one({
                '基准站站名': dict_zm[i], '地市': xx_ds, '基准站IP': i,
                '基准站名称': xx_name, '运行时长': xx_time, '纬度（度）': xx_avglat, '经度（度）': xx_avglon, '高度（米）': xx_avght,
                '跟踪到的卫星数（颗）': xx_numfixsvs, '接收机SN号': xx_serial, '天线盘SN号': xx_antennaserial, '天线类型': xx_antennatype,
                '天线高（米）': xx_antennaheight, '磁盘剩余空间（兆）': xx_surplusspace, '磁盘总空间（兆）': xx_totalspace,
                '温度（°C）': xx_celsius, '剩余电量（%）': xx_capacity, '以太网MAC地址': xx_mac, 'Bluetooth MAC地址': xx_btaddr,
                '固件版本': xx_fwversion, '启动版本': xx_monversion, '天线数据库版本': xx_antennaini, '硬件版本': xx_hwversion,
                '输出': xx_dksc_join, '运行状态': '运行正常'
            })
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm[i], xx_ds, i, xx_name, xx_time, xx_avglat, xx_avglon, xx_avght, xx_numfixsvs, xx_serial,
                 xx_antennaserial, xx_antennatype, xx_antennaheight, xx_surplusspace, xx_totalspace, xx_celsius,
                 xx_capacity, xx_mac, xx_btaddr, xx_fwversion, xx_monversion, xx_antennaini, xx_hwversion, xx_dksc_join,
                 "运行正常"))
            conn.commit()
        except ReadTimeout as e:
            print('请求超时:', i)  # 网络延时率的测试
            jsj.insert_one({
                '基准站站名': dict_zm[i], '地市': xx_ds, '基准站IP': i,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '请求超时'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm[i], xx_ds, i, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "请求超时"))
            conn.commit()
        except ConnectionError as e:
            print('网络连接异常:', i)  # 网络出现故障，连接异常
            jsj.insert_one({
                '基准站站名': dict_zm[i], '地市': xx_ds, '基准站IP': i,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm[i], xx_ds, i, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "网络连接异常"))
            conn.commit()
        except RequestException as e:
            print('请求失败:', i)
            jsj.insert_one({
                '基准站站名': dict_zm[i], '地市': xx_ds, '基准站IP': i,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '请求失败'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm[i], xx_ds, i, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "请求失败"))
            conn.commit()
    list_IP_2 = ["http://172.30.24.129/", "http://172.30.24.1/"]  # 哈尔滨站、海伦站
    dict_zm_2 = {"http://172.30.24.129/": "哈尔滨基准站", "http://172.30.24.1/": "海伦基准站"}  # 哈尔滨站、海伦站
    dict_ds_2 = {"哈尔滨基准站": "哈尔滨市", "海伦基准站": "绥化市"}
    for h in list_IP_2:
        try:
            str_1_2 = 'xml/dynamic/merge.xml?svData=&dataLogger=&ioConfigData=&powerData=&connStatus='
            str_2_2 = 'xml/dynamic/merge.xml?sysData=&options='
            str_5_2 = 'xml/dynamic/merge.xml?ioConfigData=&configData='
            url_1_2 = h + str_1_2
            url_2_2 = h + str_2_2
            url_5_2 = h + str_5_2
            # # 用于pycharm查看用
            res1_2 = requests.get(url_1_2, timeout=20)
            res2_2 = requests.get(url_2_2, timeout=20)
            res1_2.encoding = 'utf-8'
            res2_2.encoding = 'utf-8'
            soup_1_2 = BeautifulSoup(res1_2.text, 'html.parser')
            soup_2_2 = BeautifulSoup(res2_2.text, 'html.parser')
            cachedir = str(soup_2_2.select('cachedir')[0].text)
            # print(cachedir)
            str_3_jc_2 = '/xml/dynamic/posData.xml'
            str_4_jc_2 = '/xml/dynamic/merge.xml?&options=&configData='
            str_3_2 = cachedir + str_3_jc_2
            str_4_2 = cachedir + str_4_jc_2
            url_3_2 = h + str_3_2
            url_4_2 = h + str_4_2
            # print(url_1_2)
            # print(url_2_2)
            # print( url_3_2)
            # print(url_4_2)
            # print(url_5_2)
            res3_2 = requests.get(url_3_2, timeout=20)
            res4_2 = requests.get(url_4_2, timeout=20)
            res5_2 = requests.get(url_5_2, timeout=20)
            res3_2.encoding = 'utf-8'
            res4_2.encoding = 'utf-8'
            res5_2.encoding = 'utf-8'
            soup_3_2 = BeautifulSoup(res3_2.text, 'html.parser')
            soup_4_2 = BeautifulSoup(res4_2.text, 'html.parser')
            soup_5_2 = BeautifulSoup(res5_2.text, 'html.parser')
            soup_1_space_2 = int(soup_1_2.select('available')[0].text)  # 提取剩余空间
            soup_1_space_2 = (soup_1_space_2 / (1024 * 1024))  # 将剩余空间转为单位‘兆’
            soup_3_time_day_2 = int(soup_3_2.select('avgtimedays')[0].text)
            soup_3_time_hour_2 = int(soup_3_2.select('avgtimehr')[0].text)
            soup_3_time_min_2 = int(soup_3_2.select('avgtimemins')[0].text)
            soup_3_time_second_2 = int(soup_3_2.select('avgtimesecs')[0].text)
            list_SC_2 = soup_5_2.select('stream')
            # print(list_SC_2)
            xx_name_2 = str(soup_2_2.select('ownerstring1')[0].text)  # 提取基准站名称
            xx_time_day_2 = str(soup_3_time_day_2) + '日'
            xx_time_hour_2 = str(soup_3_time_hour_2) + '时'
            xx_time_min_2 = str(soup_3_time_min_2) + '分'
            xx_time_second_2 = str(soup_3_time_second_2) + '秒'
            xx_time_2 = xx_time_day_2 + xx_time_hour_2 + xx_time_min_2 + xx_time_second_2  # 计算基准站运行时长，并提取
            xx_avglat_2 = float(soup_3_2.select('avglat')[0].text)  # 提取基准站纬度
            xx_avglon_2 = float(soup_3_2.select('avglon')[0].text)  # 提取基准站经度
            xx_avght_2 = str(soup_3_2.select('avght')[0].text)  # 提取基准站高度
            xx_numfixsvs_2 = str(soup_3_2.select('numfixsvs')[0].text)  # 提取基准站跟踪的卫星数
            xx_serial_2 = str(soup_2_2.select('serial')[0].text)  # 提取接收机SN号
            xx_antennaserial_2 = str(soup_4_2.select('antennaserial')[0].text)  # 提取天线盘SN号
            xx_antennatype_2 = str(soup_4_2.select('antennatype')[0].text)  # 提取天线类型
            xx_antennaheight_2 = str(soup_4_2.select('antennaheight')[0].text)  # 提取天线高
            xx_surplusspace_2 = int(soup_1_space_2)  # 提取磁盘剩余空间
            total_space = int(soup_1_2.select('size')[0].text)
            xx_totalspace_2 = int(total_space / (1024 * 1024))  # 提取磁盘总空间
            xx_celsius_2 = float(soup_1_2.select('celsius')[0].text)  # 提取接收机温度
            xx_capacity_2 = float(soup_1_2.select('capacity')[0].text)  # 提取接收机剩余电量
            xx_mac_2 = str(soup_2_2.select('mac')[0].text)  # 提取接收机以太网MAC地址
            xx_btaddr_2 = str(soup_2_2.select('btaddr')[0].text)  # 提取接收机Bluetooth MAC地址
            xx_fwversion_2 = float(soup_2_2.select('fwversion')[0].text)  # 提取接收机固件版本
            xx_monversion_2 = float(soup_2_2.select('monversion')[0].text)  # 提取接收机启动版本
            xx_antennaini_2 = float(soup_2_2.select('antennaini')[0].text)  # 提取接收机天线数据库版本
            xx_hwversion_2 = float(soup_2_2.select('hwversion')[0].text)  # 提取接收机硬件版本
            list_dksc_2 = []  # 新建接收机端口输出列表
            for k in range(len(list_SC_2)):
                try:
                    # print('输出：',list_SC[j].select('type')[0].text,'(',list_SC[j].select('port')[0].text,')','-',list_SC[j].select('output')[0].text)
                    xx_dksc_type_2 = str(list_SC_2[k].select('type')[0].text)
                    xx_dksc_port_2 = str(list_SC_2[k].select('port')[0].text)
                    xx_dksc_output_2 = str(list_SC_2[k].select('output')[0].text)
                    xx_dksc_2 = xx_dksc_type_2 + '(' + xx_dksc_port_2 + ')' + '-' + xx_dksc_output_2
                    xx_list_dksc_2 = list_dksc_2.append(xx_dksc_2)
                except:
                    pass
            xx_dksc_join_2 = ';'.join(list_dksc_2)  # 将列表中的信息进行合并处理
            jzzmc_2 = dict_zm_2[h]  # 从字典中获取基准站名称
            xx_ds_2 = dict_ds_2[jzzmc_2]  # 从字典中获取基准站所在地
            time.sleep(1)
            jsj.insert_one({
                '基准站站名': dict_zm_2[h], '地市': xx_ds_2, '基准站IP': h,
                '基准站名称': xx_name_2, '运行时长': xx_time_2, '纬度（度）': xx_avglat_2, '经度（度）': xx_avglon_2, '高度（米）': xx_avght_2,
                '跟踪到的卫星数（颗）': xx_numfixsvs_2, '接收机SN号': xx_serial_2, '天线盘SN号': xx_antennaserial_2,
                '天线类型': xx_antennatype_2,
                '天线高（米）': xx_antennaheight_2, '磁盘剩余空间（兆）': xx_surplusspace_2, '磁盘总空间（兆）': xx_totalspace_2,
                '温度（°C）': xx_celsius_2, '剩余电量（%）': xx_capacity_2, '以太网MAC地址': xx_mac_2, 'Bluetooth MAC地址': xx_btaddr_2,
                '固件版本': xx_fwversion_2, '启动版本': xx_monversion_2, '天线数据库版本': xx_antennaini_2, '硬件版本': xx_hwversion_2,
                '输出': xx_dksc_join_2, '运行状态': '运行正常'
            })
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm_2[h], xx_ds_2, h, xx_name_2, xx_time_2, xx_avglat_2, xx_avglon_2, xx_avght_2, xx_numfixsvs_2,
                 xx_serial_2, xx_antennaserial_2, xx_antennatype_2, xx_antennaheight_2, xx_surplusspace_2,
                 xx_totalspace_2, xx_celsius_2, xx_capacity_2, xx_mac_2, xx_btaddr_2, xx_fwversion_2, xx_monversion_2,
                 xx_antennaini_2, xx_hwversion_2, xx_dksc_join_2, "运行正常"))
            conn.commit()
        except ReadTimeout as e:
            print('请求超时:', i)  # 网络延时率的测试
            jsj.insert_one({
                '基准站站名': dict_zm_2[h], '地市': xx_ds_2, '基准站IP': h,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '请求超时'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm_2[h], xx_ds_2, h, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "请求超时"))
            conn.commit()
        except ConnectionError as e:
            print('网络连接异常:', i)  # 网络出现故障，连接异常
            jsj.insert_one({
                '基准站站名': dict_zm_2[h], '地市': xx_ds_2, '基准站IP': h,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm_2[h], xx_ds_2, h, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "网络连接异常"))
            conn.commit()
        except RequestException as e:
            print('请求失败:', i)
            jsj.insert_one({
                '基准站站名': dict_zm_2[h], '地市': xx_ds_2, '基准站IP': h,
                '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL',
                '跟踪到的卫星数（颗）': 'NULL', '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
                '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
                '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
                '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '请求失败'})
            cursor.execute(
                f"insert into  {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (dict_zm_2[h], xx_ds_2, h, "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
                 "请求失败"))
            conn.commit()
    # 爬取大庆3座基准站
    username = "admin"
    password = "password"
    # 大庆基准站网站信息
    url_dq_1 = "http://173.18.32.101/CACHEDIR1549814807/xml/dynamic/merge.xml?svData=&dataLogger=&ioConfigData=&powerData=&connStatus="
    url_dq_2 = "http://173.18.32.101/CACHEDIR1549814807/xml/dynamic/merge.xml?sysData=&options="
    url_dq_5 = "http://173.18.32.101/CACHEDIR1549814807/xml/dynamic/merge.xml?ioConfigData=&configData="
    url_dq_3 = "http://173.18.32.101/CACHEDIR1549814807/xml/dynamic/posData.xml"
    url_dq_4 = "http://173.18.32.101/CACHEDIR1549814807/xml/dynamic/merge.xml?&options=&configData="
    # 大同基准站网站信息
    url_dt_1 = "http://173.18.32.104/CACHEDIR1549814807/xml/dynamic/merge.xml?svData=&dataLogger=&ioConfigData=&powerData=&connStatus="
    url_dt_2 = "http://173.18.32.104/CACHEDIR1549814807/xml/dynamic/merge.xml?sysData=&options="
    url_dt_5 = "http://173.18.32.104/CACHEDIR1549814807/xml/dynamic/merge.xml?ioConfigData=&configData="
    url_dt_3 = "http://173.18.32.104/CACHEDIR1549814807/xml/dynamic/posData.xml"
    url_dt_4 = "http://173.18.32.104/CACHEDIR1549814807/xml/dynamic/merge.xml?&options=&configData="
    # 林甸基准站网站信息
    url_ld_1 = "http://173.18.32.105/CACHEDIR1549814807/xml/dynamic/merge.xml?svData=&dataLogger=&ioConfigData=&powerData=&connStatus="
    url_ld_2 = "http://173.18.32.105/CACHEDIR1549814807/xml/dynamic/merge.xml?sysData=&options="
    url_ld_5 = "http://173.18.32.105/CACHEDIR1549814807/xml/dynamic/merge.xml?ioConfigData=&configData="
    url_ld_3 = "http://173.18.32.105/CACHEDIR1549814807/xml/dynamic/posData.xml"
    url_ld_4 = "http://173.18.32.105/CACHEDIR1549814807/xml/dynamic/merge.xml?&options=&configData="

    def Func(url_dq, username, password):
        try:
            # 创建一个密码管理者
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            # 添加用户名和密码
            password_mgr.add_password(None, url_dq, username, password)
            # 创建了一个新的handler
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            # 创建 "opener"
            opener = urllib.request.build_opener(handler)
            # 使用 opener 获取一个URL
            opener.open(url_dq)
            # 安装 opener.
            urllib.request.install_opener(opener)
            # urllib2.urlopen 使用上面的opener.
            ret = urllib.request.urlopen(url_dq)
            return ret.read()
        except urllib.error.HTTPError as e:
            if e.code == 401:
                return "authorization failed"
            else:
                raise e
        except:
            return None

    try:  # 提取大庆基准站信息
        res_dq_1 = Func(url_dq_1, username, password)
        res_dq_2 = Func(url_dq_2, username, password)
        res_dq_5 = Func(url_dq_5, username, password)
        res_dq_3 = Func(url_dq_3, username, password)
        res_dq_4 = Func(url_dq_4, username, password)
        soup_dq_1 = BeautifulSoup(res_dq_1, 'html.parser')
        soup_dq_2 = BeautifulSoup(res_dq_2, 'html.parser')
        soup_dq_5 = BeautifulSoup(res_dq_5, 'html.parser')
        soup_dq_3 = BeautifulSoup(res_dq_3, 'html.parser')
        soup_dq_4 = BeautifulSoup(res_dq_4, 'html.parser')
        # print(soup_dq_1)
        # print(soup_dq_2)
        # print(soup_dq_5)
        # print(soup_dq_3)
        # print(soup_dq_4)
        soup_1_space_dq = int(soup_dq_1.select('available')[0].text)
        soup_1_space_dq = (soup_1_space_dq / (1024 * 1024))
        soup_1_time_day_dq = int(soup_dq_1.select('day')[0].text)
        soup_1_time_hour_dq = int(soup_dq_1.select('hour')[0].text)
        soup_1_time_min_dq = int(soup_dq_1.select('min')[0].text)
        soup_1_time_second_dq = int(soup_dq_1.select('sec')[1].text)
        list_SC_dq = soup_dq_5.select('stream')
        xx_name_dq = str(soup_dq_2.select('ownerstring1')[0].text)  # 提取基准站名称
        xx_time_day_dq = str(soup_1_time_day_dq) + '日'
        xx_time_hour_dq = str(soup_1_time_hour_dq) + '时'
        xx_time_min_dq = str(soup_1_time_min_dq) + '分'
        xx_time_second_dq = str(soup_1_time_second_dq) + '秒'
        xx_time_dq = xx_time_day_dq + xx_time_hour_dq + xx_time_min_dq + xx_time_second_dq  # 计算基准站运行时长，并提取
        xx_avglat_dq = float(soup_dq_3.select('avglat')[0].text)  # 提取基准站纬度
        xx_avglon_dq = float(soup_dq_3.select('avglon')[0].text)  # 提取基准站经度
        xx_avght_dq = str(soup_dq_3.select('avght')[0].text)  # 提取基准站高度
        xx_numfixsvs_dq = str(soup_dq_3.select('numfixsvs')[0].text)  # 提取基准站跟踪的卫星数
        xx_serial_dq = str(soup_dq_2.select('serial')[0].text)  # 提取接收机SN号
        xx_antennaserial_dq = str(soup_dq_4.select('antennaserial')[0].text)  # 提取天线盘SN号
        xx_antennatype_dq = str(soup_dq_4.select('antennatype')[0].text)  # 提取天线类型
        xx_antennaheight_dq = str(soup_dq_4.select('antennaheight')[0].text)  # 提取天线高
        xx_surplusspace_dq = int(soup_1_space_dq)  # 提取磁盘剩余空间
        xx_totalspace_dq_1 = int(soup_dq_1.select('size')[0].text)  # 提取磁盘总空间
        xx_totalspace_dq_1 = (xx_totalspace_dq_1 / (1024 * 1024))  # 提取磁盘总空间\换算
        xx_totalspace_dq = int(xx_totalspace_dq_1)  # 输出
        xx_celsius_dq = float(soup_dq_1.select('celsius')[0].text)  # 提取接收机温度
        xx_capacity_dq = float(soup_dq_1.select('capacity')[0].text)  # 提取接收机剩余电量
        xx_mac_dq = str(soup_dq_2.select('mac')[0].text)  # 提取接收机以太网MAC地址
        # xx_btaddr_dq = str(soup_dq_2.select('size')[0].text)  # 提取接收机Bluetooth MAC地址
        xx_fwversion_dq = float(soup_dq_2.select('fwversion')[0].text)  # 提取接收机固件版本
        xx_monversion_dq = float(soup_dq_2.select('monversion')[0].text)  # 提取接收机启动版本
        xx_antennaini_dq = float(soup_dq_2.select('antennaini')[0].text)  # 提取接收机天线数据库版本
        xx_hwversion_dq = float(soup_dq_2.select('hwversion')[0].text)  # 提取接收机硬件版本
        list_dksc = []  # 新建接收机端口输出列表
        for j in range(len(list_SC_dq)):
            try:
                # print('输出：',list_SC[j].select('type')[0].text,'(',list_SC[j].select('port')[0].text,')','-',list_SC[j].select('output')[0].text)
                xx_dksc_type = str(list_SC_dq[j].select('type')[0].text)
                xx_dksc_port = str(list_SC_dq[j].select('port')[0].text)
                xx_dksc_output = str(list_SC_dq[j].select('output')[0].text)
                xx_dksc = xx_dksc_type + '(' + xx_dksc_port + ')' + '-' + xx_dksc_output
                xx_list_dksc = list_dksc.append(xx_dksc)
                xx_dksc_join_dq = ';'.join(list_dksc)
            except:
                pass
        jsj.insert_one({
            '基准站站名': '大庆基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.101/',
            '基准站名称': xx_name_dq, '运行时长': xx_time_dq, '纬度（度）': xx_avglat_dq, '经度（度）': xx_avglon_dq, '高度（米）': xx_avght_dq,
            '跟踪到的卫星数（颗）': xx_numfixsvs_dq, '接收机SN号': xx_serial_dq, '天线盘SN号': xx_antennaserial_dq,
            '天线类型': xx_antennatype_dq,
            '天线高（米）': xx_antennaheight_dq, '磁盘剩余空间（兆）': xx_surplusspace_dq, '磁盘总空间（兆）': xx_totalspace_dq,
            '温度（°C）': xx_celsius_dq, '剩余电量（%）': xx_capacity_dq, '以太网MAC地址': xx_mac_dq, 'Bluetooth MAC地址': 'NULL',
            '固件版本': xx_fwversion_dq, '启动版本': xx_monversion_dq, '天线数据库版本': xx_antennaini_dq, '硬件版本': xx_hwversion_dq,
            '输出': xx_dksc_join_dq, '运行状态': '运行正常'
        })
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大庆基准站', '大庆市', 'http://173.18.32.101/', xx_name_dq, xx_time_dq, xx_avglat_dq, xx_avglon_dq, xx_avght_dq,
             xx_numfixsvs_dq, xx_serial_dq, xx_antennaserial_dq, xx_antennatype_dq, xx_antennaheight_dq,
             xx_surplusspace_dq, xx_totalspace_dq, xx_celsius_dq, xx_capacity_dq, xx_mac_dq, 'NULL', xx_fwversion_dq,
             xx_monversion_dq, xx_antennaini_dq, xx_hwversion_dq, xx_dksc_join_dq, "运行正常"))
        conn.commit()
    except ReadTimeout as e:
        print('请求超时:', i)  # 网络延时率的测试
        jsj.insert_one({
            '基准站站名': '大庆基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.101/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大庆基准站', '大庆市', 'http://173.18.32.101/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求超时"))
        conn.commit()
    except ConnectionError as e:
        print('网络连接异常:', i)  # 网络出现故障，连接异常
        jsj.insert_one({
            '基准站站名': '大庆基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.101/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大庆基准站', '大庆市', 'http://173.18.32.101/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "网络连接异常"))
        conn.commit()
    except RequestException as e:
        print('请求失败:', i)
        jsj.insert_one({
            '基准站站名': '大庆基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.101/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大庆基准站', '大庆市', 'http://173.18.32.101/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求失败"))
        conn.commit()
    try:  # 提取大同基准站信息
        res_dt_1 = Func(url_dt_1, username, password)
        res_dt_2 = Func(url_dt_2, username, password)
        res_dt_5 = Func(url_dt_5, username, password)
        res_dt_3 = Func(url_dt_3, username, password)
        res_dt_4 = Func(url_dt_4, username, password)
        soup_dt_1 = BeautifulSoup(res_dt_1, 'html.parser')
        soup_dt_2 = BeautifulSoup(res_dt_2, 'html.parser')
        soup_dt_5 = BeautifulSoup(res_dt_5, 'html.parser')
        soup_dt_3 = BeautifulSoup(res_dt_3, 'html.parser')
        soup_dt_4 = BeautifulSoup(res_dt_4, 'html.parser')
        # print(soup_dt_1)
        # print(soup_dt_2)
        # print(soup_dt_5)
        # print(soup_dt_3)
        # print(soup_dt_4)
        soup_1_space_dt = int(soup_dt_1.select('available')[0].text)
        soup_1_space_dt = (soup_1_space_dt / (1024 * 1024))
        soup_1_time_day_dt = int(soup_dt_1.select('day')[0].text)
        soup_1_time_hour_dt = int(soup_dt_1.select('hour')[0].text)
        soup_1_time_min_dt = int(soup_dt_1.select('min')[0].text)
        soup_1_time_second_dt = int(soup_dt_1.select('sec')[1].text)
        list_SC_dt = soup_dt_5.select('stream')
        xx_name_dt = str(soup_dt_2.select('ownerstring1')[0].text)  # 提取基准站名称
        xx_time_day_dt = str(soup_1_time_day_dt) + '日'
        xx_time_hour_dt = str(soup_1_time_hour_dt) + '时'
        xx_time_min_dt = str(soup_1_time_min_dt) + '分'
        xx_time_second_dt = str(soup_1_time_second_dt) + '秒'
        xx_time_dt = xx_time_day_dt + xx_time_hour_dt + xx_time_min_dt + xx_time_second_dt  # 计算基准站运行时长，并提取
        xx_avglat_dt = float(soup_dt_3.select('avglat')[0].text)  # 提取基准站纬度
        xx_avglon_dt = float(soup_dt_3.select('avglon')[0].text)  # 提取基准站经度
        xx_avght_dt = str(soup_dt_3.select('avght')[0].text)  # 提取基准站高度
        xx_numfixsvs_dt = str(soup_dt_3.select('numfixsvs')[0].text)  # 提取基准站跟踪的卫星数
        xx_serial_dt = str(soup_dt_2.select('serial')[0].text)  # 提取接收机SN号
        xx_antennaserial_dt = str(soup_dt_4.select('antennaserial')[0].text)  # 提取天线盘SN号
        xx_antennatype_dt = str(soup_dt_4.select('antennatype')[0].text)  # 提取天线类型
        xx_antennaheight_dt = str(soup_dt_4.select('antennaheight')[0].text)  # 提取天线高
        xx_surplusspace_dt = int(soup_1_space_dt)  # 提取磁盘剩余空间
        xx_totalspace_dt_1 = int(soup_dt_1.select('size')[0].text)  # 提取磁盘总空间
        xx_totalspace_dt_1 = (xx_totalspace_dt_1 / (1024 * 1024))  # 提取磁盘总空间\换算
        xx_totalspace_dt = int(xx_totalspace_dt_1)  # 输出
        xx_celsius_dt = float(soup_dt_1.select('celsius')[0].text)  # 提取接收机温度
        xx_capacity_dt = float(soup_dt_1.select('capacity')[0].text)  # 提取接收机剩余电量
        xx_mac_dt = str(soup_dt_2.select('mac')[0].text)  # 提取接收机以太网MAC地址
        # xx_btaddr_dt = str(soup_dt_2.select('size')[0].text)  # 提取接收机Bluetooth MAC地址
        xx_fwversion_dt = float(soup_dt_2.select('fwversion')[0].text)  # 提取接收机固件版本
        xx_monversion_dt = float(soup_dt_2.select('monversion')[0].text)  # 提取接收机启动版本
        xx_antennaini_dt = float(soup_dt_2.select('antennaini')[0].text)  # 提取接收机天线数据库版本
        xx_hwversion_dt = float(soup_dt_2.select('hwversion')[0].text)  # 提取接收机硬件版本
        list_dksc = []  # 新建接收机端口输出列表
        for j in range(len(list_SC_dt)):
            try:
                # print('输出：',list_SC[j].select('type')[0].text,'(',list_SC[j].select('port')[0].text,')','-',list_SC[j].select('output')[0].text)
                xx_dksc_type = str(list_SC_dt[j].select('type')[0].text)
                xx_dksc_port = str(list_SC_dt[j].select('port')[0].text)
                xx_dksc_output = str(list_SC_dt[j].select('output')[0].text)
                xx_dksc = xx_dksc_type + '(' + xx_dksc_port + ')' + '-' + xx_dksc_output
                xx_list_dksc = list_dksc.append(xx_dksc)
                xx_dksc_join_dt = ';'.join(list_dksc)
            except:
                pass
        jsj.insert_one({
            '基准站站名': '大同基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.104/',
            '基准站名称': xx_name_dt, '运行时长': xx_time_dt, '纬度（度）': xx_avglat_dt, '经度（度）': xx_avglon_dt, '高度（米）': xx_avght_dt,
            '跟踪到的卫星数（颗）': xx_numfixsvs_dt, '接收机SN号': xx_serial_dt, '天线盘SN号': xx_antennaserial_dt,
            '天线类型': xx_antennatype_dt,
            '天线高（米）': xx_antennaheight_dt, '磁盘剩余空间（兆）': xx_surplusspace_dt, '磁盘总空间（兆）': xx_totalspace_dt,
            '温度（°C）': xx_celsius_dt, '剩余电量（%）': xx_capacity_dt, '以太网MAC地址': xx_mac_dt, 'Bluetooth MAC地址': 'NULL',
            '固件版本': xx_fwversion_dt, '启动版本': xx_monversion_dt, '天线数据库版本': xx_antennaini_dt, '硬件版本': xx_hwversion_dt,
            '输出': xx_dksc_join_dt, '运行状态': '运行正常'
        })
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大同基准站', '大庆市', 'http://173.18.32.104/', xx_name_dt, xx_time_dt, xx_avglat_dt, xx_avglon_dt, xx_avght_dt,
             xx_numfixsvs_dt, xx_serial_dt, xx_antennaserial_dt, xx_antennatype_dt, xx_antennaheight_dt,
             xx_surplusspace_dt, xx_totalspace_dt, xx_celsius_dt, xx_capacity_dt, xx_mac_dt, 'NULL', xx_fwversion_dt,
             xx_monversion_dt, xx_antennaini_dt, xx_hwversion_dt, xx_dksc_join_dt, "运行正常"))
        conn.commit()
    except ReadTimeout as e:
        print('请求超时:', i)  # 网络延时率的测试
        jsj.insert_one({
            '基准站站名': '大同基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.104/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大同基准站', '大庆市', 'http://173.18.32.104/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求超时"))
        conn.commit()
    except ConnectionError as e:
        print('网络连接异常:', i)  # 网络出现故障，连接异常
        jsj.insert_one({
            '基准站站名': '大同基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.104/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大同基准站', '大庆市', 'http://173.18.32.104/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "网络连接异常"))
        conn.commit()
    except RequestException as e:
        print('请求失败:', i)
        jsj.insert_one({
            '基准站站名': '大同基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.104/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('大同基准站', '大庆市', 'http://173.18.32.104/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求失败"))
        conn.commit()
    try:  # 提取林甸基准站信息
        res_ld_1 = Func(url_ld_1, username, password)
        res_ld_2 = Func(url_ld_2, username, password)
        res_ld_5 = Func(url_ld_5, username, password)
        res_ld_3 = Func(url_ld_3, username, password)
        res_ld_4 = Func(url_ld_4, username, password)
        soup_ld_1 = BeautifulSoup(res_ld_1, 'html.parser')
        soup_ld_2 = BeautifulSoup(res_ld_2, 'html.parser')
        soup_ld_5 = BeautifulSoup(res_ld_5, 'html.parser')
        soup_ld_3 = BeautifulSoup(res_ld_3, 'html.parser')
        soup_ld_4 = BeautifulSoup(res_ld_4, 'html.parser')
        # print(soup_ld_1)
        # print(soup_ld_2)
        # print(soup_ld_5)
        # print(soup_ld_3)
        # print(soup_ld_4)
        soup_1_space_ld = int(soup_ld_1.select('available')[0].text)
        soup_1_space_ld = (soup_1_space_ld / (1024 * 1024))
        soup_1_time_day_ld = int(soup_ld_1.select('day')[0].text)
        soup_1_time_hour_ld = int(soup_ld_1.select('hour')[0].text)
        soup_1_time_min_ld = int(soup_ld_1.select('min')[0].text)
        soup_1_time_second_ld = int(soup_ld_1.select('sec')[1].text)
        list_SC_ld = soup_ld_5.select('stream')
        xx_name_ld = str(soup_ld_2.select('ownerstring1')[0].text)  # 提取基准站名称
        xx_time_day_ld = str(soup_1_time_day_ld) + '日'
        xx_time_hour_ld = str(soup_1_time_hour_ld) + '时'
        xx_time_min_ld = str(soup_1_time_min_ld) + '分'
        xx_time_second_ld = str(soup_1_time_second_ld) + '秒'
        xx_time_ld = xx_time_day_ld + xx_time_hour_ld + xx_time_min_ld + xx_time_second_ld  # 计算基准站运行时长，并提取
        xx_avglat_ld = float(soup_ld_3.select('avglat')[0].text)  # 提取基准站纬度
        xx_avglon_ld = float(soup_ld_3.select('avglon')[0].text)  # 提取基准站经度
        xx_avght_ld = str(soup_ld_3.select('avght')[0].text)  # 提取基准站高度
        xx_numfixsvs_ld = str(soup_ld_3.select('numfixsvs')[0].text)  # 提取基准站跟踪的卫星数
        xx_serial_ld = str(soup_ld_2.select('serial')[0].text)  # 提取接收机SN号
        xx_antennaserial_ld = str(soup_ld_4.select('antennaserial')[0].text)  # 提取天线盘SN号
        xx_antennatype_ld = str(soup_ld_4.select('antennatype')[0].text)  # 提取天线类型
        xx_antennaheight_ld = str(soup_ld_4.select('antennaheight')[0].text)  # 提取天线高
        xx_surplusspace_ld = int(soup_1_space_ld)  # 提取磁盘剩余空间
        xx_totalspace_ld_1 = int(soup_ld_1.select('size')[0].text)  # 提取磁盘总空间
        xx_totalspace_ld_1 = (xx_totalspace_ld_1 / (1024 * 1024))  # 提取磁盘总空间\换算
        xx_totalspace_ld = int(xx_totalspace_ld_1)  # 输出
        xx_celsius_ld = float(soup_ld_1.select('celsius')[0].text)  # 提取接收机温度
        xx_capacity_ld = float(soup_ld_1.select('capacity')[0].text)  # 提取接收机剩余电量
        xx_mac_ld = str(soup_ld_2.select('mac')[0].text)  # 提取接收机以太网MAC地址
        # xx_btaddr_ld = str(soup_ld_2.select('size')[0].text)  # 提取接收机Bluetooth MAC地址
        xx_fwversion_ld = float(soup_ld_2.select('fwversion')[0].text)  # 提取接收机固件版本
        xx_monversion_ld = float(soup_ld_2.select('monversion')[0].text)  # 提取接收机启动版本
        xx_antennaini_ld = float(soup_ld_2.select('antennaini')[0].text)  # 提取接收机天线数据库版本
        xx_hwversion_ld = float(soup_ld_2.select('hwversion')[0].text)  # 提取接收机硬件版本
        list_dksc = []  # 新建接收机端口输出列表
        for j in range(len(list_SC_ld)):
            try:
                # print('输出：',list_SC[j].select('type')[0].text,'(',list_SC[j].select('port')[0].text,')','-',list_SC[j].select('output')[0].text)
                xx_dksc_type = str(list_SC_ld[j].select('type')[0].text)
                xx_dksc_port = str(list_SC_ld[j].select('port')[0].text)
                xx_dksc_output = str(list_SC_ld[j].select('output')[0].text)
                xx_dksc = xx_dksc_type + '(' + xx_dksc_port + ')' + '-' + xx_dksc_output
                xx_list_dksc = list_dksc.append(xx_dksc)
                xx_dksc_join_ld = ';'.join(list_dksc)
            except:
                pass
        jsj.insert_one({
            '基准站站名': '林甸基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.105/',
            '基准站名称': xx_name_ld, '运行时长': xx_time_ld, '纬度（度）': xx_avglat_ld, '经度（度）': xx_avglon_ld, '高度（米）': xx_avght_ld,
            '跟踪到的卫星数（颗）': xx_numfixsvs_ld, '接收机SN号': xx_serial_ld, '天线盘SN号': xx_antennaserial_ld,
            '天线类型': xx_antennatype_ld,
            '天线高（米）': xx_antennaheight_ld, '磁盘剩余空间（兆）': xx_surplusspace_ld, '磁盘总空间（兆）': xx_totalspace_ld,
            '温度（°C）': xx_celsius_ld, '剩余电量（%）': xx_capacity_ld, '以太网MAC地址': xx_mac_ld, 'Bluetooth MAC地址': 'NULL',
            '固件版本': xx_fwversion_ld, '启动版本': xx_monversion_ld, '天线数据库版本': xx_antennaini_ld, '硬件版本': xx_hwversion_ld,
            '输出': xx_dksc_join_ld, '运行状态': '运行正常'
        })
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('林甸基准站', '大庆市', 'http://173.18.32.105/', xx_name_ld, xx_time_ld, xx_avglat_ld, xx_avglon_ld, xx_avght_ld,
             xx_numfixsvs_ld, xx_serial_ld, xx_antennaserial_ld, xx_antennatype_ld, xx_antennaheight_ld,
             xx_surplusspace_ld, xx_totalspace_ld, xx_celsius_ld, xx_capacity_ld, xx_mac_ld, 'NULL', xx_fwversion_ld,
             xx_monversion_ld, xx_antennaini_ld, xx_hwversion_ld, xx_dksc_join_ld, "运行正常"))
        conn.commit()
    except ReadTimeout as e:
        print('请求超时:', i)  # 网络延时率的测试
        jsj.insert_one({
            '基准站站名': '林甸基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.105/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('林甸基准站', '大庆市', 'http://173.18.32.105/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求超时"))
        conn.commit()
    except ConnectionError as e:
        print('网络连接异常:', i)  # 网络出现故障，连接异常
        jsj.insert_one({
            '基准站站名': '林甸基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.105/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('林甸基准站', '大庆市', 'http://173.18.32.105/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "网络连接异常"))
        conn.commit()
    except RequestException as e:
        print('请求失败:', i)
        jsj.insert_one({
            '基准站站名': '林甸基准站', '地市': '大庆市', '基准站IP': 'http://173.18.32.105/',
            '基准站名称': 'NULL', '运行时长': 'NULL', '纬度（度）': 'NULL', '经度（度）': 'NULL', '高度（米）': 'NULL', '跟踪到的卫星数（颗）': 'NULL',
            '接收机SN号': 'NULL', '天线盘SN号': 'NULL', '天线类型': 'NULL',
            '天线高（米）': 'NULL', '磁盘剩余空间（兆）': 'NULL', '磁盘总空间（兆）': 'NULL', '温度（°C）': 'NULL', '剩余电量（%）': 'NULL',
            '以太网MAC地址': 'NULL', 'Bluetooth MAC地址': 'NULL',
            '固件版本': 'NULL', '启动版本': 'NULL', '天线数据库版本': 'NULL', '硬件版本': 'NULL', '输出': 'NULL', '运行状态': '网络连接异常'})
        cursor.execute(
            f"insert into {today_table_name}(基准站站名,地市,基准站IP,基准站名称,运行时长,纬度（度）,经度（度）,高度（米）,跟踪到的卫星数（颗）,接收机SN号,天线盘SN号,天线类型,天线高（米）,磁盘剩余空间（兆）,磁盘总空间（兆）,温度（°C）,剩余电量,以太网MAC地址,蓝牙MAC地址,固件版本,启动版本,天线数据库版本,硬件版本,输出,运行状态) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            ('林甸基准站', '大庆市', 'http://173.18.32.105/', "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL", "NULL",
             "请求失败"))
        conn.commit()
    # res_dq_1=Func(url_dq_1, username, password)
    # soup_dq_1 = BeautifulSoup(res_dq_1, 'html.parser')
    # print(soup_dq_1)
    # xx_name_ld = str(soup_dq_1.text)
    # print(xx_name_ld)
    # list1 = xx_name_ld.split('[#|]')
    # print(list1)
    # print(list1[0])

    # print(soup_dq_1)
    # print(soup_dq_2)
    # print(soup_dq_5)
    # print(soup_dq_3)
    # print(soup_dq_4)







