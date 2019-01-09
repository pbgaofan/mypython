def stationinformation():
    import xlwt
    import pymongo
    import csv
    from datetime import date  # ### 新增

    # 初始化数据库
    mongo_url = "127.0.0.1:27017"
    DATABASE = "hljcors基准站ups状态数据"
    # TABLE = "ups20181206"   # ### 注释掉了
    today_str = date.today().strftime(
        '%Y%m%d')  # ###新增 获取当天日期，并转成字符串YYYYMMDD的格式
    TABLE = f"ups{today_str}"  # ### 新增
    client = pymongo.MongoClient(mongo_url)
    db_des = client[DATABASE]
    db_des_table = db_des[TABLE]
    # 将数据写入到CSV文件中
    # 如果直接从mongod booster导出, 一旦有部分出现字段缺失，那么会出现结果错位的问题
    # newline='' 的作用是防止结果数据中出现空行，专属于python3
    with open(f"{DATABASE}_{TABLE}.csv", "w", newline='') as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        # 先写列名
        # 写第一行，字段名
        fieldList = [
            "_id",
            "基准站站名",
            "输入电压",
            "输出电压",
            "最大输出电压",
            "最小输出电压",
            "频率（赫兹）",
            "总电压",
            "电池容量",
            "温度",
            "运行状态",
        ]
        writer.writerow(fieldList)
        allRecordRes = db_des_table.find()
        # 写入多行数据
        for record in allRecordRes:
            print(f"record = {record}")
            recordValueLst = []
            for field in fieldList:
                if field not in record:
                    recordValueLst.append("None")
                else:
                    recordValueLst.append(record[field])
            try:
                writer.writerow(recordValueLst)
            except Exception as e:
                print(f"write csv exception. e = {e}")
        # 初始化数据库
    with open(f'hljcors基准站ups状态数据_ups{today_str}.csv', 'r') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')  # 创建一个sheet表格
        l = 0
        for line in read:
            print(line)
            r = 0
            for i in line:
                print(i)
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1
        workbook.save('不间断电源状态信息.xlsx')  # 保存Excel
    mongo_url = "127.0.0.1:27017"
    DATABASE = "hljcors基准站接收机状态数据"
    # TABLE = "jsj20181206"   # ###注释掉了
    TABLE = f"jsj{today_str}"  # ### 新增
    client = pymongo.MongoClient(mongo_url)
    db_des = client[DATABASE]
    db_des_table = db_des[TABLE]
    # 将数据写入到CSV文件中
    # 如果直接从mongod booster导出, 一旦有部分出现字段缺失，那么会出现结果错位的问题
    # newline='' 的作用是防止结果数据中出现空行，专属于python3
    with open(f"{DATABASE}_{TABLE}.csv", "w", newline='') as csvfileWriter:
        writer = csv.writer(csvfileWriter)
        # 先写列名
        # 写第一行，字段名
        fieldList = [
            "_id",
            "基准站站名",
            "地市",
            "基准站IP",
            "基准站名称",
            "运行时长",
            "纬度（度）",
            "经度（度）",
            "高度（米）",
            "跟踪到的卫星数（颗）",
            "接收机SN号",
            "天线类型",
            "天线高（米）",
            "磁盘剩余空间（兆）",
            "磁盘总空间（兆）",
            "温度（°C）",
            "剩余电量（%）",
            "以太网MAC地址",
            "Bluetooth MAC地址",
            "固件版本",
            "启动版本",
            "天线数据库版本",
            "硬件版本",
            "输出",
            "运行状态",
        ]
        writer.writerow(fieldList)
        allRecordRes = db_des_table.find()
        # 写入多行数据
        for record in allRecordRes:
            print(f"record = {record}")
            recordValueLst = []
            for field in fieldList:
                if field not in record:
                    recordValueLst.append("None")
                else:
                    recordValueLst.append(record[field])
            try:
                writer.writerow(recordValueLst)
            except Exception as e:
                print(f"write csv exception. e = {e}")
    with open(f'hljcors基准站接收机状态数据_jsj{today_str}.csv', 'r') as f:
        read = csv.reader(f)
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('data')  # 创建一个sheet表格
        l = 0
        for line in read:
            print(line)
            r = 0
            for i in line:
                print(i)
                sheet.write(l, r, i)  # 一个一个将单元格数据写入
                r = r + 1
            l = l + 1
        workbook.save('接收机状态信息.xlsx')  # 保存Excel
