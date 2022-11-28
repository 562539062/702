#  11-18 Fri. A new UI needed to be designed

import tkinter as tk
from matplotlib.figure import Figure
from sys import exit
import numpy as np
import create_excel as ex
import tkinter.messagebox as messagebox
import os


from tkinter import Canvas, ttk,Frame,filedialog,HORIZONTAL
from threading import Thread
from fnmatch import fnmatch
from time import time,strftime,localtime
import multiprocessing
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.ticker as ticker
import datetime
import matplotlib.pyplot as plt # test

import functions as fc
import settings as s
from Calender import Calendar
from  UI_variables import *
from plot import plot_tj, plot_Osig
from exceptional_handling import handle

class UI_only:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title('船舶项目——数据前处理')
        self.sw = self.root.winfo_screenwidth() # 屏幕宽度
        self.sh = self.root.winfo_screenheight() # 屏幕高度
        self.root.state('normal')
        self.root.resizable(0,0) #防止用户调整尺寸
        self.root.maxsize(self.sw, self.sh)
        self.propool=multiprocessing.Pool() # 进程池初始化
        # 左半边底    
        self.module_left = Frame(self.root)
        self.module_left.pack(in_=self.root, fill='y', side='left',expand=tk.YES)
        self.pix_height = self.module_left.winfo_screenheight()
        # 右半边底
        self.module_right = Frame(self.root)
        self.module_right.pack(in_=self.root, fill='y', side='left',expand=tk.YES)
        nowtime=str(datetime.datetime.now())
        self.sp=nowtime[0:4]+nowtime[5:7]+nowtime[8:10]
        self.ep=self.sp


        
        self.setting_module() # Settings模块
        self.view_module() # 查看Excel, 图像
        # self.root.after(100, self.plot_button)

        # ……
        # 异常处理
        self.root.protocol("WM_DELETE_WINDOW",self.shutdown)
        self.root.mainloop()
        pass

        
    def shutdown(self):
        exit(0)
        #销毁root窗口

    def setting_module(self):
        #### 运行前的设置模块  ####
        self.frame_setting = Frame(self.module_left, borderwidth=5,highlightbackground="Grey", highlightthickness=3, relief='groove') # settings 模块对象
        self.frame_setting.pack(in_=self.module_left, fill='both',anchor='nw',ipadx=8, ipady=3, padx=1, pady=2) #

        #### grid (row = 0, column = 0~5)已占用, 为模块标题  ####
        setting_label = tk.Label(self.frame_setting,
                                text = "运行前Settings:",
                                font=('bold', 20),
                                relief="ridge",
                                anchor='center') # title
        setting_label.grid(row = 0, column = 0, columnspan=6,ipadx=8,ipady=8, sticky="nesw")

        #### grid (row = 1~3, column = 0~5)已占用, 为settings  ####
        row_settings = [1,2,3]
        self.SFreq_entry = self.make_entrys(layer = self.frame_setting, name_text = '信号频率(Hz)', trow = row_settings[0] , tcolumn = 0, default_val = 50)
        self.Slen_entry = self.make_entrys(layer = self.frame_setting, name_text = '每段数据长度', trow = row_settings[0] , tcolumn = 2, default_val = 90000)
        self.Slen_entry_ = self.make_entrys(layer = self.frame_setting, name_text = '数据总长度', trow = row_settings[0] , tcolumn = 4, default_val = 720000)
        self.FF_entry = self.make_entrys(layer = self.frame_setting, name_text = '低频极限(Hz)', trow = row_settings[1] , tcolumn = 0, default_val = 0.01)
        self.forcenum_entry = self.make_entrys(layer = self.frame_setting, name_text = '单向应力数量(个)', trow = row_settings[1] , tcolumn = 2, default_val = 10)
        self.F1_entry = self.make_entrys(layer = self.frame_setting, name_text = '慢飘成分起始频率(Hz)', trow = row_settings[1] , tcolumn = 4, default_val = 0.01)
        self.F2_enrty = self.make_entrys(layer = self.frame_setting, name_text = '波浪成分起始频率(Hz)', trow = row_settings[2] , tcolumn = 0, default_val = 0.095)
        self.F3_entry = self.make_entrys(layer = self.frame_setting, name_text = '信号高频起始频率(Hz)', trow = row_settings[2] , tcolumn = 2, default_val = 0.5)
        self.F4_entry = self.make_entrys(layer = self.frame_setting, name_text = '信号高频结束频率(Hz)', trow = row_settings[2] , tcolumn = 4, default_val = 7)
        self.click_flag = False # 默认是不会被改变的
        
        
        #### grid (row = 4, column = 0~5)已占用, 为run_path 文件路径  ####
        self.run_path = tk.StringVar() # 数据处理路径
        row_runPath = 4
        label_path = tk.Label(self.frame_setting,text = "* 文件夹路径:")
        label_path.grid(row = row_runPath, column = 0, sticky='E', pady=6)
        #输入框绑定变量run_path
        run_path_entry = tk.Entry(self.frame_setting ,textvariable=self.run_path, width=55)
        run_path_entry.grid(row = row_runPath, column = 1, columnspan = 4, sticky='w')
        #button 跳转选择路径  
        path_button_run = tk.Button(self.frame_setting, text = '路径选择', width=8, command = self.selectRunPath)
        path_button_run.grid(row = row_runPath, column = 5, padx=3)
        # path_button_run.bind('<Button-1>',func=self.selectRunPath)

         #### grid (row = 4, column = 0~5)已占用, 为run_path 文件路径  ####
        self.savepath = tk.StringVar() # 数据处理路径
        self.savepath.set(os.path.abspath(os.path.join(os.getcwd(), "../save")))
        row_savePath = 5
        label_path = tk.Label(self.frame_setting,text = "* 保存路径:")
        label_path.grid(row = row_savePath, column = 0, sticky='E', pady=6)
        #输入框绑定变量run_path
        run_path_entry = tk.Entry(self.frame_setting ,textvariable=self.savepath, width=55)
        run_path_entry.grid(row = row_savePath, column = 1, columnspan = 4, sticky='w')
        #button 跳转选择路径  
        path_button_run = tk.Button(self.frame_setting, text = '路径选择', width=8, command = self.selectSavePath)
        path_button_run.grid(row = row_savePath, column = 5, padx=3)

        #### grid (row = 5, column = 0~4)已占用, 为data_type 下拉框  ####
        row_dataType = 6
        self.data_type = self.make_combobox(layer = self.frame_setting, name_text = "* 数据类型:", trow = row_dataType, tcolumn = 0,twidth = 37, default_val = data_types, tstate='readonly')

        #### grid (row = 5-6, column = 5)已占用, 为运行 button 和终止 button  ####
        run_button = tk.Button(self.frame_setting, text = '运行', width=8, command = self.run_check_thread)
        run_button.grid(row = row_dataType, column = 5 , padx=3)
        stop_button = tk.Button(self.frame_setting, text = '终止', width=8, command = self.stop_run)
        stop_button.grid(row = row_dataType + 1, column = 5, padx=3)


        #### grid (row = 6, column = 0~5)已占用, 为run_dataEntry 日期选择框  ####
        row_data = 7
        self.run_startDate, self.run_endDate = self.make_dataEntry(self.frame_setting, trow = row_data, tcolumn = 0,twidth=12)

        #### grid (row = 7, column = 0~5)已占用, 为运行进度条  ####
        row_progBar = 8
        self.progressbarOne = ttk.Progressbar(self.frame_setting,length=600,mode="indeterminate",orient=HORIZONTAL)
        self.progressbarOne.grid(row=row_progBar, columnspan=6, pady=6)
        
        

    

    def view_module(self):
        self.frame_viewSetting = Frame(self.module_left, borderwidth=5,highlightbackground="Grey", highlightthickness=3,relief='groove') # view选项 模块
        self.frame_viewSetting.pack(after=self.frame_setting, fill='both',anchor='nw',ipadx=8, ipady=3, padx=1, pady=2)

        #### 模块标题  ####
        viewSet_label = tk.Label(self.frame_viewSetting,
                                text = "运行后view:",
                                font=('bold', 20),
                                relief='ridge',
                                anchor='center') # title
        viewSet_label.grid(row = 0,column=0,columnspan=2,ipadx=2, ipady=3, padx=4, pady=2,sticky="news")
        
        #### choice ####
        self.choice = Frame(self.frame_viewSetting,borderwidth=3, highlightbackground="Grey", highlightthickness=1,relief='flat')
        self.choice.grid_configure(in_=self.frame_viewSetting, row = 1,column=0, ipadx=8, ipady=3, padx=4, pady=5, sticky='we')
        # 信号名下拉框 grid(1, 0~4)
        row_signalName = 1
        self.signal_name = self.make_combobox(self.choice,"* 信号名:", trow=row_signalName, tcolumn=0,twidth=8,default_val=[x for x in Signame if x not in delname])
        
        # 特殊值的勾选框 grid(2~4, 0~2) eg: Peak_max_wave
        row_speVal = 2
        text1 = ["全幅值","峰值","谷值"]
        text2 = ["平均值","有义值","最大值"]
        text3 = ["合成成分","高频成分","波浪成分"]
        
        self.var1 = []
        for text in text1:
            i  = text1.index(text)
            self.var1.append(tk.IntVar())
            fullr1 = tk.Checkbutton(self.choice, text=text, variable=self.var1[-1], state='normal')
            fullr1.grid(row=row_speVal, column=i, sticky='W')
        self.var2 = []
        for text in text2:
            i  = text2.index(text)
            self.var2.append(tk.IntVar())
            fullr2 = tk.Checkbutton(self.choice, text=text, variable=self.var2[-1], state='normal')
            # fullr2.deselect()
            fullr2.grid(row=row_speVal+1, column=i, sticky='W')
        self.var3 = []
        for text in text3:
            i  = text3.index(text)
            self.var3.append(tk.IntVar())
            fullr3 = tk.Checkbutton(self.choice, text=text, variable=self.var3[-1], state='normal')
            # fullr3.deselect()
            fullr3.grid(row=row_speVal+2, column=i, sticky='W')

        #### Excel查看 #### 
        self.excelView = Frame(self.frame_viewSetting,borderwidth=3,highlightbackground="Grey", highlightthickness=1,relief='flat')
        self.excelView.grid_configure(in_=self.frame_viewSetting, row=1,column=1, ipadx=8, ipady=3, padx=2, pady=5)
        # titile grid(0,0~3)
        excel_label = tk.Label(self.excelView,
                                text = "View Excel:",
                                font=('bold', 15),
                                relief="ridge",
                                anchor='center') # title
        excel_label.grid(row=0,columnspan=6,padx=2, pady=10, sticky='news')
        
        # 日期选择 grid(1, 0~3)
        row_periodExcel = 1
        self.excel_start, self.excel_end = self.make_dataEntry(self.excelView, trow = row_periodExcel, tcolumn = 0)

        # period 按钮 grid(2, 0~5)
        excelButton = 2
        period_button = tk.Button(self.excelView, text = 'Period Btn', width=20, command=lambda:self.show_excel(0))
        period_button.grid(row = excelButton, column = 0, columnspan=3 , padx=2, pady=6)
        # period_button.bind('<Button-1>',func=self.show_excel)
        sum_button = tk.Button(self.excelView, text = '汇总 Btn', width=20, command=lambda:self.show_excel(1))
        sum_button.grid(row = excelButton, column = 3, columnspan=3 , padx=2, pady=6)
        # sum_button.bind('<Button-1>',func=self.show_excel)

        #### 图像查看 #### 
        self.plotView = Frame(self.frame_viewSetting,borderwidth=3,highlightbackground="Grey", highlightthickness=1,relief='flat')
        self.plotView.grid_configure(in_=self.frame_viewSetting, row=2,columnspan=2, ipadx=8, ipady=3, padx=2, pady=5)
        # titile grid(0,0~3)
        plot_label = tk.Label(self.plotView,
                                text = "View image:",
                                font=('bold', 15),
                                relief="ridge",
                                anchor='center') # title
        plot_label.grid(row=0,columnspan=10,padx=2, pady=10, sticky='news')
    
        # 日期选择 grid(1, 0~6)
        row_periodPlot = 1
        label_path = tk.Label(self.plotView,text = "* 该项查看指定日期、指定信号的特殊值:")
        label_path.grid(row = row_periodPlot, column = 0, sticky='E', pady=6)
        self.plot_start, self.plot_end = self.make_dataEntry(self.plotView, trow = row_periodPlot, tcolumn = 1)
        
        # 绘制 指定信号名及特殊值 的图像 grid(1, 7~9)
        plotButton = 1
        period_PlotButton = tk.Button(self.plotView, text = '查看图像', width=10, command = self.plot_button)
        period_PlotButton.grid(row = plotButton, column = 7, columnspan=3 , padx=2, pady=6)
        # period_PlotButton.bind('<Button-1>',func=self.show_excel)
        
        # grid (row = 2, column = 0~5)已占用, 为异常处理EHPlot
        self.EHPlot_path = tk.StringVar() # 数据处理路径
        row_EHPlot= 2
        label_path = tk.Label(self.plotView,text = "* 信号异常文件路径:")
        label_path.grid(row = row_EHPlot, column = 0, sticky='E', pady=6)
        # grid (row = 3, column = 0~5)已占用, 为异常处理EHPlot
        #输入框绑定变量run_path
        EHP_path_entry = tk.Entry(self.plotView ,textvariable=self.EHPlot_path, width=33)
        EHP_path_entry.grid(row = row_EHPlot, column = 1, columnspan = 5, sticky='w')
        #button 跳转选择路径  
        path_button_EHPlot = tk.Button(self.plotView, text = '路径选择', width=8, command = self.selectEHPlotPath)
        path_button_EHPlot.grid(row = row_EHPlot, column = 5, padx=3)


        # EHPlot 设置 grid(4, 1~ )
        EHplot_sets = 3
        self.polyfig_len = self.make_entrys(layer = self.plotView, name_text = '拟合分段长度', trow= EHplot_sets, tcolumn = 0, default_val=3000)
        self.threshold = self.make_entrys(layer = self.plotView, name_text = '阈值', trow= EHplot_sets, tcolumn = 2, default_val=3)
        self.circulation = self.make_entrys(layer = self.plotView, name_text = '拟合循环次数', trow= EHplot_sets+1, tcolumn = 0, default_val=1)
        self.segment_len = self.make_entrys(layer = self.plotView, name_text = 'Segment', trow= EHplot_sets+1, tcolumn = 2, default_val=720000)

        # 绘制 指定信号名及特殊值 的图像 grid(1, 7~9)
        EHPlot_button = tk.Button(self.plotView, text = '处理图像', width=8,height=2, command = self.excp_handl)
        EHPlot_button.grid(row = EHplot_sets, column = 5, rowspan=2 , padx=2, pady=6)
        # EHPlot_button.bind('<Button-1>',func=self.show_excel)
        
        
        
        ##################右侧图片展示#######################
        self.frame_plot = Frame(self.module_right, borderwidth=5,highlightbackground="Grey", highlightthickness=3,relief='groove') # view选项 模块
        self.frame_plot.pack(fill='both',anchor='w',ipadx=8, ipady=3, padx=1, pady=2,expand=tk.YES)

        #### 模块标题  ####
        viewPlot_label = tk.Label(self.frame_plot,
                                text = "Plot图像:",
                                font=('bold', 20),
                                relief='ridge',
                                anchor='center') # title
        # viewPlot_label.grid(row = 0,column=0,columnspan=2,ipadx=2, ipady=3, padx=4, pady=2,sticky="news")
        viewPlot_label.pack(side=tk.TOP,  # 上对齐
                            anchor='center',  # 填充方式
                            expand=tk.YES)  # 随窗口大小调整而调整

        self.canvas = Canvas()
        fig_init = Figure(figsize=(10, 6), dpi=100)
        fig_init.add_subplot(111)
        
        self.create_form(fig_init)



    def create_form(self,figure):
        '''把绘制的图形figure渲染到tkinter窗口上'''
        self.output=FigureCanvasTkAgg(figure,self.frame_plot)
        self.output.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
        self.output.get_tk_widget().pack(side=tk.TOP,  # 上对齐
                                    fill=tk.BOTH,  # 填充方式
                                    expand=tk.YES)  # 随窗口大小调整而调整
        self.output.mpl_connect('scroll_event', self.mouse_scoll)
        #把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        
        self.output._tkcanvas.pack(side=tk.TOP,  # get_tk_widget()得到的就是_tkcanvas
                            fill=tk.BOTH,
                            expand=tk.YES)

    

    def show_excel(self,flag):
        if flag==0 and (self.check_var(self.var1) == False or self.check_var(self.var2) == False or self.check_var(self.var3) == False):
            messagebox.showinfo(title='show information', message='漏选')
            return False
        else:
            select_check = []
            vars = self.var1 + self.var2 + self.var3
            for i in vars:
                select_check.append(i.get())
                
        runfiles=self.files_in_period(self.excel_start.get(),self.excel_end.get())
        if runfiles==[]:
            messagebox.showinfo(title='show information', message='No data exists in the selected time range. \n'\
                                'Please run the calculation first to get the result data or check whether the source data exists in this time period')
            return False
        savepath=self.savepath.get()+'/'
        if flag:
            ex.gen_excel(savepath,runfiles,np.ones(9),s.index_3)
        else:
            select_point_index=[s.Signame.index(self.signal_name.get())]
            ex.gen_excel(savepath,runfiles,select_check,select_point_index)


    def make_entrys(self, layer, name_text, trow, tcolumn, default_val):
        ''' 每个enrty占两列
        标签名  trow行 tcolumn列 '''
        label_SFreq = tk.Label(layer, text=name_text+':')
        label_SFreq.grid(row = trow, column = tcolumn, sticky="E", padx=6, pady=6)
        # 输入框 （trow行 tcolumn+1列）
        temp_entry = tk.Entry(layer, width=8 ,relief="sunken")
        # temp_entry.bind('<Return>',func=self.print_it) # 绑定回车事件，响应func=
        temp_entry.grid(row = trow, column = tcolumn+1)
        temp_entry.insert(0, default_val)
        temp_entry.bind('<Button-1>', func=self.click_entry)
        return temp_entry

    def make_combobox(self, layer, name_text, trow, tcolumn, twidth, default_val, tstate=''):
        # 每个combobox占6行
        # 标签名 （trow行 tcolumn列）
        label_signalname = tk.Label(layer,text = name_text)
        label_signalname.grid(row = trow, column = tcolumn,sticky="E", pady=6)
        # 下拉框 （trow行 tcolumn+1 列, columnspan=5）
        temp_combobox = ttk.Combobox(
            master=layer,  # 父容器
            height=5,  # 高度,下拉显示的条目数量
            width=twidth,  # 宽度
            state='',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 15),  # 字体、字号
            textvariable='',  # 通过StringVar设置可改变的值
            values=default_val,  # 设置下拉框的选项
            )
        temp_combobox.bind("<<ComboboxSelected>>", self.print_it)
        temp_combobox.grid(row = trow, column = tcolumn+1, columnspan=4,sticky='w')
        return temp_combobox

    def make_dataEntry(self, layer, trow, tcolumn, twidth = 10):
        self.output_img_flag = 1 # 日期已默认被选择
        width, height = layer.winfo_reqwidth() + 50, 50 #窗口大小
        x, y = (layer.winfo_screenwidth()  - width )/2, (layer.winfo_screenheight() - height)/2#居中位置
        ww = 800
        wh = 400
        #开始日期
        date_startv = tk.StringVar() #开始日期存于该字符串
        date_startv.set(self.sp[0:4]+'-'+self.sp[4:6]+'-'+self.sp[6:8])
        temp_dateStart = ttk.Entry(layer, textvariable = date_startv, width=twidth, justify='center')
        temp_dateStart.grid(row=trow,column=tcolumn+1,columnspan=2,sticky='w')
        sdate_str_gain = lambda: [
            date_startv.set(date)
            for date in [Calendar((x-ww/3, y+wh/5),int(self.sp[0:4]),int(self.sp[4:6]), 'ur').selection()] 
            if date]
        self.sdate_bu=tk.Button(layer, text = '* 开始日期:', command = sdate_str_gain)
        self.sdate_bu.grid(row=trow,column=tcolumn, sticky='e', padx= 6)

        #截止日期
        date_endv = tk.StringVar() #截至日期存于该字符串
        date_endv.set(self.ep[0:4]+'-'+self.ep[4:6]+'-'+self.ep[6:8])
        temp_dateEnd = ttk.Entry(layer, textvariable = date_endv, width=twidth, justify='center')
        temp_dateEnd.grid(row=trow,column=tcolumn+4,columnspan=2,sticky='w')
        edate_str_gain = lambda: [
            date_endv.set(date)
            for date in [Calendar((x-ww/3, y+wh/5),int(self.ep[0:4]),int(self.ep[4:6]), 'ur').selection()] 
            if date]
        self.edate_bu=tk.Button(layer, text = '* 截止日期:', command = edate_str_gain)
        self.edate_bu.grid(row=trow,column=tcolumn+3,sticky='e', padx= 6)
        return temp_dateStart, temp_dateEnd

    def print_it(self, *args):
        print(self.data_type.get())

    def selectRunPath(self):
        # 选择文件path_接收文件地址
        path = filedialog.askdirectory(initialdir='../')
        #通过replace函数替换绝对文件地址中的/来使文件可被程序读取 
        #注意：\\转义后为\，所以\\\\转义后为\\
        temp_path=path.replace("/","\\\\")
        self.run_path.set(temp_path)
        sum=os.listdir(temp_path)
        self.sp=sum[0]
        self.ep=sum[-1]

    def selectSavePath(self):
        # 选择文件path_接收文件地址
        path = filedialog.askdirectory(initialdir='../save/')
        self.savepath.set(path)

    def selectEHPlotPath(self):
        # 选择文件path_接收文件地址
        path = filedialog.askopenfile(initialdir='../')
        self.EHPlot_path.set(path.name)

    def click_entry(self):
        # 是否修改过entry, 认为点击过即修改过
        self.click_flag = True
        
######################检查main所需参数以及对运行创建线程###############################
    def run_check_thread(self):
        ############## Check dataType is needed (check filenames?)#########
        self.setting_values = Setting_Values()
        if self.run_path.get() and self.data_type.get():
            print(self.run_path.get())
        elif self.data_type.get() == '':
            messagebox.showinfo(title='Error', message='数据类型不能为空，请选择数据类型！')
            return 1
        elif self.run_path.get() == '':
            messagebox.showinfo(title='Error', message='文件夹路径不能为空，请选择文件夹！')
            return 1
        elif self.click_flag == True:
            # 运行run_main 有设置修改 
            tempValue_list = [self.SFreq_entry.get(),self.Slen_entry.get(),self.Slen_entry_.get(),self.FF_entry.get(),self.forcenum_entry.get(),self.F1_entry.get(),self.F2_enrty.get(),self.F3_entry.get(),self.F4_entry.get()]
            self.setting_values.modify(tempValue_list)
        self.main_thread = Thread(target=self.start_main)
        # self.msg_queue.put(main_thread)
        self.main_thread.daemon=True
        self.main_thread.start()
    
    def stop_run(self):
        self.propool.terminate()
        self.main_thread.join(2)
        self.progressbarOne.stop()

        
        # self.main_thread.
    ##############运行signal2计算功能#############################
    def start_main(self):
        self.progressbarOne.start()
        self.propool=multiprocessing.Pool()
        runfiles=self.files_in_period(self.run_startDate.get(),self.run_endDate.get())
        savepath=self.savepath.get()+'/'
        runpath=self.run_path.get()
        start_t=time()
        args_list=[]
        realrunfiles=[]
        sumS=fc.getfileseg(runfiles)
        for fn in range(len(runfiles)):
            if os.path.exists(savepath + 'plot_data/A1/'+runfiles[fn]):
                print(runfiles[fn]+'\'s data already exists')
            else:       
                #用于多进程的共享数据存储segment段数数据的存储，以便运行完毕之后按顺序存数据
                for Sigment in range(1,sumS[fn]+1):
                    args_list.append([runpath,runfiles[fn],savepath,Sigment,self.setting_values])
                realrunfiles.append(runfiles[fn])
        if not len(args_list)==0:
            try:
                result=self.propool.map(fc.signal2,args_list)
                self.propool.close()
                self.propool.join()
                fc.pddeal(savepath,realrunfiles,result)
            except:
                self.propool.terminate()
                print('进程池内出错或被终止！')
                messagebox.showinfo(title='Error', message='傻逼出错了,自己改BUG去吧!!!')
        self.progressbarOne.stop()
        end_t=time()
        print(end_t-start_t)
        messagebox.showinfo(title='show information', message='run finish')
        
###################选择时间内的文件夹########################
    def files_in_period(self,sp,ep):
        startdate=sp[0:4]+sp[5:7]+sp[8:]
        enddate=str(int(ep[0:4]+ep[5:7]+ep[8:])+1)
        runfiles=[]
        flag=0
        sumfiles=os.listdir(self.run_path.get())
        if int(enddate)<int(sumfiles[0][0:8]) :
            return runfiles
        elif int(startdate)<int(sumfiles[0][0:8]):
            startdate=sumfiles[0][0:8]
        for f_name in sumfiles:
            if fnmatch(f_name, startdate+'*'):
                flag=1
            if fnmatch(f_name, enddate+'*'):
                break
            if flag==1:
                runfiles.append(f_name)
        return runfiles
##########################画图按钮功能###########################
    def plot_button(self, *args):
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        if (self.signal_name.get() and self.check_values()):
            # 将日期转换为int，比较所选日期是否已保存数据，没数据的日期不能画图
            date_start = int(str(str(self.plot_start.get())[0:4]+str(self.plot_start.get())[5:7]+str(self.plot_start.get())[8:]))
            date_end = int(str(str(self.plot_end.get())[0:4]+str(self.plot_end.get())[5:7]+str(self.plot_end.get())[8:]))
            path_temp = os.path.join(self.savepath.get()+ "/plot_data/" + self.signal_name.get()+'/')
            path_list = os.listdir(path=path_temp)
            t_start = int(str(path_list[0])[0:8])
            t_end = int(str(path_list[-1])[0:8])
            if date_start >= t_start and date_end <= t_end:
                # self.output.get_tk_widget().delete()
                self.output._tkcanvas.destroy()
                fig = plt.figure()
                plot_tj(self.signal_name.get(), self.var_string, self.plot_start.get(), self.plot_end.get(), self.savepath.get() + '/plot_data/')
                # fig.gca().xaxis.set_major_locator(ticker.AutoLocator())
                self.create_form(fig)
                toolbar =NavigationToolbar2Tk(self.output, self.frame_plot) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
                toolbar.update()
            else:
                messagebox.showinfo(title='Error', message='数据不全！\n请重新选择日期 或 运行该时间段后查看')
        elif not self.signal_name.get():
            messagebox.showinfo(title='Error', message='请选择信号名！')
        else:
            messagebox.showinfo(title='Error', message='请选择一种完整值（如：波浪成分 全幅值的有义值）！')


    def check_var(self, var_n): # 检查特殊值的某一行是否全未选择
        temp_list = 0
        for i in range(len(var_n)):
            if var_n[i].get() == 0:
                temp_list += 1
        if temp_list == len(var_n):
            return False
        else:
            return True

    def check_values(self): # 检查特殊值是否存在一行留空了
        if self.check_var(self.var1) == False or self.check_var(self.var2) == False or self.check_var(self.var3) == False:
            return False
        else:
            self.var_string = []
            vars = self.var1 + self.var2 + self.var3
            for i in vars:
                self.var_string.append(i.get())
            return True

    def mouse_scoll(self, event):
        '''Needed to be fixed'''
        current_ax = event.inaxes

        x_min, x_max = current_ax.get_xlim()
        y_min, y_max = current_ax.get_ylim()

        x_step = (x_max-x_min)/10
        y_step = (y_max-y_min)/10

        if event.button == "up":
            current_ax.set(xlim=(x_min+x_step,x_max-x_step),ylim=(y_min+y_step, y_max-y_step))
        elif event.button == "down":
            current_ax.set(xlim=(x_min-x_step,x_max+x_step),ylim=(y_min-y_step, y_max+y_step))
        self.output.draw_idle()

    def excp_handl(self):
        # 点击画图，清除画布
        for widget in self.frame_plot.winfo_children():
            widget.destroy()
        [x1, y1] = plot_Osig(path=self.EHPlot_path.get(), segment=int(self.segment_len.get()))
        [x2, y2] = handle(name=self.EHPlot_path.get(),index=int(self.polyfig_len.get()),delta=int(self.threshold.get()),n=int(self.circulation.get()),segment=int(self.segment_len.get()))
        fig = plt.figure()
        plt.subplot(2,1,1)#截取幕布的一部分
        plt.plot(x1, y1)
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        plt.subplot(2,1,2)
        plt.plot(x2, y2)
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
        self.create_form(fig)
        toolbar =NavigationToolbar2Tk(self.output, self.frame_plot) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
        toolbar.update()
        
        


if __name__ == '__main__':
    # multiprocessing.freeze_support()
    a = UI_only()
    