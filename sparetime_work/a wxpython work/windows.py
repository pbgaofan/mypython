import pymysql
from datetime import date
import datetime
import wx    #导入wxpython
import datetime
import os
import sys
import pandas as pd
import wx.grid as grid


nowtime = datetime.datetime.now().strftime('%F %T')
RECEIVER_EXCEL_PATH=os.path.join(sys.path[0],'接收机状态信息.xlsx')
POWER_INFO_EXCEL_PAHH=os.path.join(sys.path[0],'不间断电源状态信息.xlsx')

class MyFrame(wx.Frame):
    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,title="HLJCORS基准站监测系统",pos=(300,100),size=(710,500))   #界面的设置参数 高度增加了100
        panel = wx.Panel(self)   #创建画板
        panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBack)
        title= wx.StaticText(panel,label = '欢迎使用HLJCORS基准站监测系统',pos = (10,10))#添加TEXT文档
        font = wx.Font(14,wx.DEFAULT,wx.FONTSTYLE_NORMAL,wx.NORMAL)
        title.SetFont(font)
        #self.m_staticText1 = wx.StaticText(panel, wx.ID_ANY, "接收机正常运行个数：", (40, 40))
        #self.m_staticText2 = wx.StaticText(panel, wx.ID_ANY, "基准站故障个数：", (40, 60))
        #self.m_staticText3 = wx.StaticText(panel, wx.ID_ANY, "不间断电源正常运行个数：", (40, 80))
        #self.m_staticText4 = wx.StaticText(panel, wx.ID_ANY, "不间断电源故障个数：", (40, 100))
        #self.m_staticText2.SetForegroundColour('#FF0000')
        #self.m_staticText4.SetForegroundColour('#FF0000')
        #self.bt_today_station = wx.Button(panel, wx.ID_ANY, label='今日基准站状态信息', pos=(40, 280), size=(120, 40))  # 添加Button按钮
        self.bt_receiver = wx.Button(panel, wx.ID_ANY, label='当前接收机状态信息', pos=(100, 280), size=(120, 40))  # 添加Button按钮
        self.bt_ups= wx.Button(panel, wx.ID_ANY, label='当前不间断电源状态信息', pos=(300, 280), size=(160, 40))  # 添加Button按钮
        #self.bt_today_station.Bind(wx.EVT_BUTTON,self.Onclick_bt_today_station)            #添加单击事件
        self.bt_receiver.Bind(wx.EVT_BUTTON,self.Onclick_bt_receiver)            #添加单击事件
        self.bt_ups.Bind(wx.EVT_BUTTON,self.Onclick_bt_ups)
        #self.bt_today_station.SetForegroundColour('#6F4242')                 #添加背景颜色
        #self.bt_today_station.SetBackgroundColour('WHITE')
        self.bt_receiver.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_receiver.SetBackgroundColour('WHITE')
        self.bt_ups.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_ups.SetBackgroundColour('WHITE')
        self.bt_read_receiver = wx.Button(panel, wx.ID_ANY, label='读取接收机状态信息', pos=(100, 330), size=(120, 40))  # ###新增
        self.bt_read_powerinfo=wx.Button(panel,wx.ID_ANY, label='读取当前不间断电源状态信息', pos=(300, 330), size=(160, 40)) # ###新增
        self.bt_read_receiver.Bind(wx.EVT_BUTTON,self.Onclick_bt_read_receiver)
        self.bt_read_powerinfo.Bind(wx.EVT_BUTTON,self.Onclick_bt_read_powerinfo)

        self.bt_read_receiver.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_read_receiver.SetBackgroundColour('WHITE')
        self.bt_read_powerinfo.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_read_powerinfo.SetBackgroundColour('WHITE')
        #创建垂直方向布局
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        self.bt_sjtq = wx.Button(panel,wx.ID_ANY,label = '接收机信息提取',pos=(560,40),size=(120,40))           #添加Button按钮
        self.bt_upssjtq = wx.Button(panel,wx.ID_ANY,label = '不间断电源信息提取',pos=(560,100),size=(120,40))           #添加Button按钮
        self.bt_rk = wx.Button(panel,wx.ID_ANY, label='信息入库', pos=(560,160),size=(120,40))
        self.bt_csv = wx.Button(panel,wx.ID_ANY, label='导出*.html文件', pos=(560,220),size=(120,40))
        self.bt_xls = wx.Button(panel,wx.ID_ANY, label='提取基准站状态信息', pos=(560,280),size=(120,40))
        self.bt_sjtq.Bind(wx.EVT_BUTTON,self.Onclick_bt_sjtq)            #添加单击事件
        self.bt_upssjtq.Bind(wx.EVT_BUTTON,self.Onclick_bt_upssjtq)            #添加单击事件
        self.bt_rk.Bind(wx.EVT_BUTTON,self.Onclick_bt_rk)
        self.bt_csv.Bind(wx.EVT_BUTTON,self.Onclick_bt_csv)
        self.bt_xls.Bind(wx.EVT_BUTTON,self.Onclick_bt_xls)
        self.bt_sjtq.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_sjtq.SetBackgroundColour('WHITE')
        self.bt_upssjtq.SetForegroundColour('#6F4242')                 #添加背景颜色
        self.bt_upssjtq.SetBackgroundColour('WHITE')
        self.bt_rk.SetForegroundColour('#6F4242')
        self.bt_rk.SetBackgroundColour('WHITE')
        self.bt_csv.SetForegroundColour('#6F4242')
        self.bt_csv.SetBackgroundColour('WHITE')
        self.bt_xls.SetForegroundColour('#6F4242')
        self.bt_xls.SetBackgroundColour('WHITE')
        panel.SetBackgroundColour('white')  # 设置面板的背景颜色
    def Onclick_bt_sjtq(self,event):
        import receiverinformation
        receiverinformation.receiver()
        #progressMax = 100
        #dialog = wx.ProgressDialog("基准站接收机信息提取中","剩余时间",progressMax,style = wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        message1 = "基准站接收机信息提取完毕"
        wx.MessageBox(message1)
    def Onclick_bt_upssjtq(self, event):
        import upsiformation
        upsiformation.ups()
        message2 = "基准站不间断电源信息提取完毕"
        wx.MessageBox(message2)
    def Onclick_bt_rk(self, event):
        import progressbar
        progressbar.bar()
        message3 = "完成入库" 
        wx.MessageBox(message3)
    def Onclick_bt_csv(self, event):
        import turnhtml
        turnhtml.turnhtml()
        message4 = "已导出*.html文件"
        wx.MessageBox(message4)
    def Onclick_bt_xls(self, event):
        import stationinformation
        stationinformation.stationinformation()
        message5 = "基准站状态信息已提取完毕"
        wx.MessageBox(message5)
        #添加容器，容器中空间横向排列
        hsizer_button = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_button.Add(self.bt_sjtq,proportion = 0,flag = wx.ALIGN_CENTER,border = 5)
        hsizer_button.Add(self.bt_rk, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_csv, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        hsizer_button.Add(self.bt_xls, proportion=0, flag=wx.ALIGN_CENTER, border=5)
        #添加容器，容器中空间纵向排列
        #vsizer_all = wx.BoxSizer(wx.VERTICAL)
        #vsizer_all.Add(hsizer_button,proportion = 0,flag = wx.ALIGN_CENTER | wx.TOP,border = 15)
        #panel.SetSizer(vsizer_all)`

    def Onclick_bt_receiver(self, event):
        import pandas as pd
        excelFile = r'接收机状态信息.xlsx'
        df = pd.DataFrame(pd.read_excel(excelFile))
        # print(df)
        # df1= df[['基准站站名', '地市', '基准站IP', '基准站名称', '运行状态']]
        # print(df1)
        data = df.loc[df['运行状态'].str.contains('网络连接异常')]
        print(data)
        pmlist = data[['基准站站名']].values.T.tolist()[:][0]
        print(pmlist)
        # pmlist2 = data[['基准站IP']].values.T.tolist()[:][0]
        # print(pmlist2)
        sum_list = []
        for pm in pmlist:
            temp = []
            dfbypm = data.loc[data['基准站站名'] == pm]
            temp.append(pm)
            print(temp)
            print(dfbypm.columns)
            for col in dfbypm.columns:
                if col == '运行状态':
                    hvalue = '网络连接异常'
                    print(hvalue)
                    temp.append(hvalue)
            sum_list.append(temp)
        list_jsj = sum_list
        print(list_jsj)
        filePath = r'当前接收机故障信息.xlsx'
        summaryDataFrame = pd.DataFrame(sum_list)
        summaryDataFrame.to_excel(filePath, encoding='utf-8', index=False, header=False)
        import wx  # 导入wxpython
        import wx.grid
        column_names = ['基准站站名', '运行状态']

        class MyFrame(wx.Frame):
            def __init__(self, parent, id):
                wx.Frame.__init__(self, parent, id, title="接收机当前故障信息", pos=(500, 200), size=(250, 250))  # 界面的设置参数
                panel = wx.Panel(self)  # 创建画板
                self.grid = self.CreateGrid(self)
                self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

            def OnLabelLeftClick(self, event):
                print('RowIdx:{0}'.format(event.GetRow()))
                print('RowIdx:{0}'.format(event.GetCol()))
                print(list_jsj[event.GetRow()])
                # 确保能继续处理其他的事件
                event.Skip()

            def CreateGrid(self, parent):
                grid = wx.grid.Grid(parent)
                grid.CreateGrid(len(list_jsj), len(list_jsj[0]))
                for row in range(len(list_jsj)):
                    for col in range(len(list_jsj[row])):
                        grid.SetColLabelValue(col, column_names[col])
                        grid.SetCellValue(row, col, list_jsj[row][col])
                # 设置行和列自动调整
                grid.AutoSize()
                return grid

        class App(wx.App):
            def OnInit(self):
                frame = MyFrame
                frame.show()
                return true

            def OnExit(self):
                print("应用程序退出")
                return ()

        if __name__ == '__main__':
            app = wx.App()  # 初始化应用
            frame = MyFrame(parent=None, id=-1)  # 实例MyFrame类，并传递参数
            frame.Show()  # 显示窗口
            app.MainLoop()  # 调用MainLoop()主循环方法

    def Onclick_bt_ups(self, event):
        import pandas as pd
        excelFile = r'不间断电源状态信息.xlsx'
        df = pd.DataFrame(pd.read_excel(excelFile))
        # print(df)
        # df1= df[['基准站站名', '地市', '基准站IP', '基准站名称', '运行状态']]
        # print(df1)
        data = df.loc[df['运行状态'].str.contains('网络连接异常')]
        print(data)
        pmlist = data[['基准站站名']].values.T.tolist()[:][0]
        print(pmlist)
        # pmlist2 = data[['基准站IP']].values.T.tolist()[:][0]
        # print(pmlist2)
        sum_list = []
        for pm in pmlist:
            temp = []
            dfbypm = data.loc[data['基准站站名'] == pm]
            temp.append(pm)
            print(temp)
            print(dfbypm.columns)
            for col in dfbypm.columns:
                if col == '运行状态':
                    hvalue = '网络连接异常'
                    print(hvalue)
                    temp.append(hvalue)
            sum_list.append(temp)
        list_jsj = sum_list
        print(list_jsj)
        filePath = r'当前不间断电源状态信息.xlsx'
        summaryDataFrame = pd.DataFrame(sum_list)
        summaryDataFrame.to_excel(filePath, encoding='utf-8', index=False, header=False)
        import wx  # 导入wxpython
        import wx.grid
        column_names = ['基准站站名', '运行状态']

        class MyFrame(wx.Frame):
            def __init__(self, parent, id):
                wx.Frame.__init__(self, parent, id, title="不间断电源当前故障信息", pos=(500, 200), size=(250, 250))  # 界面的设置参数
                panel = wx.Panel(self)  # 创建画板
                self.grid = self.CreateGrid(self)
                self.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)

            def OnLabelLeftClick(self, event):
                print('RowIdx:{0}'.format(event.GetRow()))
                print('RowIdx:{0}'.format(event.GetCol()))
                print(list_jsj[event.GetRow()])
                # 确保能继续处理其他的事件
                event.Skip()

            def CreateGrid(self, parent):
                grid = wx.grid.Grid(parent)
                grid.CreateGrid(len(list_jsj), len(list_jsj[0]))
                for row in range(len(list_jsj)):
                    for col in range(len(list_jsj[row])):
                        grid.SetColLabelValue(col, column_names[col])
                        grid.SetCellValue(row, col, list_jsj[row][col])
                # 设置行和列自动调整
                grid.AutoSize()
                return grid

        class App(wx.App):
            def OnInit(self):
                frame = MyFrame
                frame.show()
                return true

            def OnExit(self):
                print("应用程序退出")
                return ()

        if __name__ == '__main__':
            app = wx.App()  # 初始化应用
            frame = MyFrame(parent=None, id=-1)  # 实例MyFrame类，并传递参数
            frame.Show()  # 显示窗口
            app.MainLoop()  # 调用MainLoop()主循环方法
    def OnEraseBack(self, event):
        dc = event.GetDC()
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        logo_path=os.path.join(sys.path[0],"logo.jpg") # ### 新增 定义LOGO图片的路径
        #bmp = wx.Bitmap("logo.jpg") 
        bmp = wx.Bitmap(logo_path) # ###加载图片修改
        dc.DrawBitmap(bmp, 0, 0)
    
    def Onclick_bt_read_receiver(self,event):          # ###新增 读取接收机状态信息.xlsx的点击函数
        self.gridframe=ReceiverGridFrame(self,-1)
    
    def Onclick_bt_read_powerinfo(self,event):        # ### 新增  读取不间断电源状态信息.xlsx的点击函数
        self.gridframe=PowerInfoGridFrame(self,-1)

class ReceiverGridFrame(wx.Frame):  # ###新增 读取接收机状态信息.xlsx

    def __init__(self, parent,id):

        wx.Frame.__init__(self, parent,id,title="接收机状态信息", pos=(500, 200), size=(710, 500))  # 界面的设置参数
        #panel = wx.Panel(self)  # 创建画板
        _grid = grid.Grid(self, -1)
        #Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        df=pd.read_excel(RECEIVER_EXCEL_PATH)
        self.df=df.loc[df['磁盘剩余空间（兆）']>1500]
        print(self.df)
        rows=len(self.df)
        cols=len(self.df.columns)
        print(rows,cols)
        _grid.CreateGrid(rows, cols)
        for i in range(cols):
            _grid.SetColLabelValue(i,str(self.df.columns[i]))
        for i in range(rows):
            for j in range(cols):
                _grid.SetCellValue(i,j,str(self.df.iloc[i][j]))
        # 设置行和列自动调整
        _grid.AutoSize()
        self.Show()
        #return _grid

class PowerInfoGridFrame(wx.Frame): # ### 新增  读取不间断电源状态信息.xlsx

    def __init__(self, parent,id):

        wx.Frame.__init__(self, parent,id,title="不间断电源状态信息.xlsx", pos=(500, 200), size=(710, 500))  # 界面的设置参数
        #panel = wx.Panel(self)  # 创建画板
        _grid = grid.Grid(self, -1)
        #Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.OnLabelLeftClick)
        df=pd.read_excel(POWER_INFO_EXCEL_PAHH)
        self.df=df[[x for x in df.columns if x!='温度']]
        rows=len(self.df)
        cols=len(self.df.columns)
        _grid.CreateGrid(rows, cols)
        for i in range(cols):
            _grid.SetColLabelValue(i,str(self.df.columns[i]))
        for i in range(rows):
            for j in range(cols):
                _grid.SetCellValue(i,j,str(self.df.iloc[i][j]))
        # 设置行和列自动调整
        _grid.AutoSize()
        self.Show()
        #return _grid


class App(wx.App):
    def OnInit (self):
        frame = MyFrame
        frame.show()
        return true
    def OnExit (self):
        print("应用程序退出")
        return()


if __name__=='__main__':
    app=wx.App()                      #初始化应用
    frame=MyFrame(parent=None,id=-1)      #实例MyFrame类，并传递参数
    frame.Show()                          #显示窗口
    app.MainLoop()                        #调用MainLoop()主循环方法


