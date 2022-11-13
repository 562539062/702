import tkinter as tk
import os
import tkinter.messagebox as messagebox
from time import time
from fnmatch import fnmatch
import multiprocessing
from multiprocessing import Process
from multiprocessing.sharedctypes import Array
from threading import Thread

from Calender import Calendar
from tkinter import ttk,Frame,filedialog
from queue import Queue

import functions as fc
import settings as s
from plot import plot

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('船舶项目 数据前处理 input')
        self.sw = self.root.winfo_screenwidth()
        #得到屏幕宽度
        self.sh = self.root.winfo_screenheight()
        #得到屏幕高度
        ww = 500
        wh = 300
        x = (self.sw-ww) / 2
        y = (self.sh-wh) / 2
        self.root.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
        self.input()
        # self.output()

    # ipnut 界面
    def input(self):
        #变量path
        self.path = tk.StringVar()
        frame_input = Frame(self.root)
        frame_input.place(relx=0.5, rely=0.5, anchor='center')
        #输入框，标记，按键
        label_path = tk.Label(frame_input,text = "文件夹路径:")
        label_path.grid(row = 0, column = 0)
        #输入框绑定变量path
        entry_path=tk.Entry(frame_input, textvariable = self.path,width=17)
        entry_path.grid(row = 0, column = 1)
        self.button_0 = tk.Button(frame_input, text = "路径选择", command = self.selectPath).grid(row = 0, column = 2)

        label_datatype = tk.Label(frame_input,text = "数据类型:")
        label_datatype.grid(row = 1, column = 0)
        data_types = ['2D-6A','科研平台','2号']
        self.combobox_0 = ttk.Combobox(
            master=frame_input,  # 父容器
            height=10,  # 高度,下拉显示的条目数量
            width=10,  # 宽度
            state='',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 15),  # 字体、字号
            textvariable='',  # 通过StringVar设置可改变的值
            values=data_types,  # 设置下拉框的选项
            )
        self.combobox_0.bind("<<ComboboxSelected>>", self.pick_datatype)
        self.combobox_0.grid(row = 1, column = 1)
        
        self.button_1 = tk.Button(frame_input,text="确定",command=self.check_button_1)
        self.button_1.bind('<Return>',self.check_button_1)
        self.button_1.grid(row=1, column=2)
        self.root.mainloop()


    def selectPath(self):
        #选择文件path_接收文件地址
        path_ = filedialog.askdirectory(initialdir='../newdata')
        #通过replace函数替换绝对文件地址中的/来使文件可被程序读取 
        #注意：\\转义后为\，所以\\\\转义后为\\
        self.path_=path_.replace("/","\\\\")
        #path设置path_的值
        self.path.set(path_)

    def check_button_1(self):
        if self.path.get() and self.combobox_0.get():
            # print(self.path.get())
            # print(" type is: ")
            # print(type(self.path.get()))
            # print(self.datatype)
            # ======================
            # filepath = self.path.get()
            # datatype = self.datatype
            # 载入数据的函数
            # @wyc
            # ======================
            self.root.destroy()
            self.output()
            # self.output_window.mainloop()
        elif self.combobox_0.get() == '':
            messagebox.showinfo(title='Error', message='数据类型不能为空，请选择数据类型！')
        else:
            messagebox.showinfo(title='Error', message='文件夹路径不能为空，请选择文件夹！')

    def pick_datatype(self,*args):
        self.datatype = self.combobox_0.get()
        print("选中的数据类型："+self.datatype)
        


    ######################################
    # output界面
    ######################################
    def output(self):
        self.output_window = tk.Tk()
        self.output_window.title('船舶项目 数据前处理 output')
        ww = 500
        wh = 300
        x = (self.sw-ww) / 2
        y = (self.sh-wh) / 2
        self.output_window.geometry("%dx%d+%d+%d" %(ww,wh,x,y))
        frame_output = Frame(self.output_window)
        frame_output.place(relx=0.5, rely=0.5, anchor='center')

        label_signalname = tk.Label(frame_output,text = "信号名:")
        label_signalname.grid(row = 0, column = 0)
        # 信号名下拉框
        signal_values = ['D1','D2','D3','D4','D5','D6','D7','D8','D9','D10','S1X','S1Y','S1Z','S2X','S2Y','S2Z','S3X','S3Y','S3Z','S4X','S4Y','S4Z','S5X','S5Y','S5Z','S6X','S6Y','S6Z','S7X','S7Y','S7Z','S8X','S8Y','S8Z','S9X','S9Y','S9Z','S10X','S10Y','S10Z','S11X','S11Y','S11Z','S12X','S12Y','S12Z','S13X','S13Y','S13Z','S14X','S14Y','S14Z','S15X','S15Y','S15Z','S16X','S16Y','S16Z','S17X','S17Y','S17Z','S18X','S18Y','S18Z','S19X','S19Y','S19Z','S20X','S20Y','S20Z','S21X','S21Y','S21Z','S22X','S22Y','S22Z','S23X','S23Y','S23Z','S24X','S24Y','S24Z','S25X','S25Y','S25Z','S26X','S26Y','S26Z','S27X','S27Y','S27Z','S28X','S28Y','S28Z','S29X','S29Y','S29Z','S30X','S30Y','S30Z','S31X','S31Y','S31Z','S32X','S32Y','S32Z','S33X','S33Y','S33Z','S34X','S34Y','S34Z','S35X','S35Y','S35Z','S36X','S36Y','S36Z','S37X','S37Y','S37Z','S38X','S38Y','S38Z','S39X','S39Y','S39Z','S40X','S40Y','S40Z','S41X','S41Y','S41Z','S42X','S42Y','S42Z','S43X','S43Y','S43Z','S44X','S44Y','S44Z','A1','A2','A3','M1-X','M1-Y','M1-Z','M1-Yaw','M1-Roll','M1-Pitch','Z1','Z31','Z32','Z4']
        self.combobox_1 = ttk.Combobox(
            master=frame_output,  # 父容器
            height=10,  # 高度,下拉显示的条目数量
            width=6,  # 宽度
            state='',  # 设置状态 normal(可选可输入)、readonly(只可选)、 disabled(禁止输入选择)
            cursor='arrow',  # 鼠标移动时样式 arrow, circle, cross, plus...
            font=('', 15),  # 字体、字号
            textvariable='',  # 通过StringVar设置可改变的值
            values=signal_values,  # 设置下拉框的选项
            )
        self.combobox_1.bind("<<ComboboxSelected>>", self.pick_signal)
        self.combobox_1.grid(row=0,column=1)
        

        # 值的勾选框 Peak_max_wave
        text1 = ["全幅值","峰值","谷值"]
        text2 = ["有义值","最大值"]
        text3 = ["合成成分","高频成分","波浪成分"]
        value1 = ['Full_',"Peak_","Valley_"]
        value2 = ["meaningful_","max_"]
        value3 = ["syn","high","wave"]
        
        
        self.var1 = tk.StringVar()
        self.var1.set(None)
        for text in text1:
            i  = text1.index(text)
            fullr1 = tk.Radiobutton(frame_output, text=text, variable=self.var1, value=value1[i], state='normal')
            fullr1.deselect()
            fullr1.grid(row=1, column=i, sticky='W')
        
        self.var2 = tk.StringVar()
        self.var2.set(None)
        for text in text2:
            i  = text2.index(text)
            fullr2 = tk.Radiobutton(frame_output, text=text, variable=self.var2, value=value2[i], state='normal')
            fullr2.deselect()
            fullr2.grid(row=3, column=i, sticky='W')

        self.var3 = tk.StringVar()
        self.var3.set(None)
        for text in text3:
            i  = text3.index(text)
            fullr3 = tk.Radiobutton(frame_output, text=text, variable=self.var3, value=value3[i], state='normal')
            fullr1.deselect()
            fullr3.grid(row=2, column=i, sticky='W')




        date_list = os.listdir(self.path.get())
        self.output_img_flag = 1 # 日期未被选择过
        width, height = frame_output.winfo_reqwidth() + 50, 50 #窗口大小
        x, y = (frame_output.winfo_screenwidth()  - width )/2, (frame_output.winfo_screenheight() - height)/2#居中位置
        
        #开始日期
        sp=str(date_list[0])
        date_startv = tk.StringVar() #开始日期存于该字符串
        date_startv.set(sp[0:4]+'-'+sp[4:6]+'-'+sp[6:8])
        self.date_start = ttk.Entry(frame_output, textvariable = date_startv, width=10)
        self.date_start.grid(row=4,column=1)
        sdate_str_gain = lambda: [
            date_startv.set(date)
            for date in [Calendar((x-ww/3, y+wh/5), 'ur').selection()] 
            if date]
        self.sdate_bu=tk.Button(frame_output, text = '开始日期:', command = sdate_str_gain)
        self.sdate_bu.grid(row=4,column=0)

        #截止日期
        ep=str(date_list[-1])
        date_endv = tk.StringVar() #截至日期存于该字符串
        date_endv.set(ep[0:4]+'-'+ep[4:6]+'-'+ep[6:8])
        self.date_end = ttk.Entry(frame_output, textvariable = date_endv, width=10)
        self.date_end.grid(row=4,column=3)
        edate_str_gain = lambda: [
            date_endv.set(date)
            for date in [Calendar((x, y+wh/5), 'ur').selection()] 
            if date]
        self.edate_bu=tk.Button(frame_output, text = '截止日期:', command = edate_str_gain)
        self.edate_bu.grid(row=4,column=2)   

        
        
        self.button_run = tk.Button(frame_output,text="运行",command=self.run)
        self.button_run.grid(row=7, column=0)


        self.button_excel = tk.Button(frame_output,text="查看Excel",command=self.check_button_excel)
        self.button_excel.grid(row=7, column=1)

        # 信号名、值 确定
        self.button_00 = tk.Button(frame_output,text="Output图像",command=self.check_button_00)
        self.button_00.grid(row=7, column=2)
        
        #进度条
        self.progressbarOne = ttk.Progressbar(frame_output,length=300)
        self.progressbarOne.grid(row=8,columnspan=4,pady=5)        
        # print(frame_output.grid_info)
        self.output_window.mainloop()
        
    def pick_signal(self, *args):
        print("选中的信号:"+ self.combobox_1.get())

#########################
    def run(self):
        main_thread = Thread(target=self.start_main)
        # self.msg_queue.put(main_thread)
        main_thread.setDaemon(True)
        main_thread.start()
########################

    def start_main(self):
        DataPath = self.path.get()
        savepath='../save/'
        sp=self.date_start.get()
        ep=self.date_end.get()
        print("ep is :"+ep)
        startdate=sp[0:4]+sp[5:7]+sp[8:]
        enddate=str(int(ep[0:4]+ep[5:7]+ep[8:])+1)
        runfiles=[]
        flag=0
        for f_name in os.listdir(DataPath):
            if fnmatch(f_name, startdate+'*'):
                flag=1
            if flag==1:
                runfiles.append(f_name)
            if fnmatch(f_name, enddate+'*'):
                break
        fc.createtimeline(runfiles)
        # 进度值最大值
        self.progressbarOne['maximum'] = len(runfiles)
        # 进度值初始值
        self.progressbarOne['value'] = 0
        # fc.preinit(savepath)
        start_t=time()
        
        for ffilename in runfiles:
            if os.path.exists('../save/excel/'+ffilename):
                print(ffilename+'\'s data already exists')
            else:       
                print('start '+ffilename+' file')
                MyProcess=[]
                MyProcess.clear()
                tempplotdata=Array('f',len(s.Signame)*len(s.pointname)*s.sumSegment)
                #用于多进程的共享数据存储segment段数数据的存储，以便运行完毕之后按顺序存数据
                for Sigment in range(1,s.sumSegment+1):
                    mypro=Process(target=fc.signal2,args=(DataPath,ffilename,savepath,Sigment,tempplotdata))
                    MyProcess.append(mypro)
                for i in MyProcess:
                    i.daemon=True
                    i.start()
                    # i.join()
                for i in MyProcess:
                    i.join()
                fc.pddeal(savepath,ffilename,tempplotdata)
                # 每次更新加1
            self.progressbarOne['value'] +=1
            # 更新画面
            # self.output_window.update()
        end_t=time()
        messagebox.showinfo(title='show information', message='run finish')
        print(end_t-start_t)
        

    def check_button_excel(self):
        excel_path = "../save/excel"
        filedialog.askopenfilename(initialdir=excel_path)




    def check_button_00(self, *args):
        if (self.combobox_1.get() and self.var1.get() != 'None' and self.var2.get() != 'None' and self.var3.get() != 'None' and self.output_img_flag == 1):
            self.var_string = str(self.var1.get())+str(self.var2.get())+str(self.var3.get())
            # 将日期转换为int，比较所选日期是否已保存数据，没数据的日期不能画图
            date_start = int(str(str(self.date_start.get())[0:4]+str(self.date_start.get())[5:7]+str(self.date_start.get())[8:]))
            date_end = int(str(str(self.date_end.get())[0:4]+str(self.date_end.get())[5:7]+str(self.date_end.get())[8:]))
            path_temp = os.path.join("../save/plot_data/"+self.combobox_1.get()+'/')
            path_list = os.listdir(path=path_temp)
            t_start = int(str(path_list[0])[0:8])
            t_end = int(str(path_list[-1])[0:8])
            if date_start >= t_start and date_end <= t_end:
                plot(self.combobox_1.get(), self.var_string,self.date_start.get(),self.date_end.get(), self.path.get())
            else:
                messagebox.showinfo(title='Error', message='数据不全！\n请重新选择日期 或 运行该时间段后查看')
        elif not self.combobox_1.get():
            messagebox.showinfo(title='Error', message='请选择信号名！')
        elif self.output_img_flag == 0:
            messagebox.showinfo(title='Error', message='请选择日期！')
        else:
            messagebox.showinfo(title='Error', message='请选择一种完整值（如：波浪成分 全幅值的有义值）！')


    def print_date(self, *args):
        self.output_img_flag = 1
        print(self.date_start.get())




if __name__ == '__main__':
    multiprocessing.freeze_support()
    a = GUI()
    