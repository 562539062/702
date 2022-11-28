from time import sleep
from tkinter import Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt # test

root= tk.Tk()
root.title('船舶项目——数据前处理')
root.state('normal')
root.resizable(0,0) #防止用户调整尺寸
# 左半边底    
module_left = Frame(root)
module_left.pack(in_=root, fill='y', side='left',expand=tk.YES)
pix_height = module_left.winfo_screenheight()
# 右半边底
module_right = Frame(root)
module_right.pack(in_=root, fill='y', side='left',expand=tk.YES)

frame_plot = Frame(module_right, borderwidth=5,highlightbackground="Grey", highlightthickness=3,relief='groove') # view选项 模块
frame_plot.pack(fill='both',anchor='w',ipadx=8, ipady=3, padx=1, pady=2,expand=tk.YES)

fig = plt.figure()
output=FigureCanvasTkAgg(fig,frame_plot)
output.draw()  #以前的版本使用show()方法，matplotlib 2.2之后不再推荐show（）用draw代替，但是用show不会报错，会显示警告
output.get_tk_widget().pack(side=tk.TOP,  # 上对齐
                            fill=tk.BOTH,  # 填充方式
                            expand=tk.YES)  # 随窗口大小调整而调整
#把matplotlib绘制图形的导航工具栏显示到tkinter窗口上

output._tkcanvas.pack(side=tk.TOP,  # get_tk_widget()得到的就是_tkcanvas
                    fill=tk.BOTH,
                    expand=tk.YES)
def shutdown():
        exit(0)
def dels():
    toolitems = NavigationToolbar2Tk.toolitems
    for i in toolitems:
        print(i)

for i in range(3):
    toolbar =NavigationToolbar2Tk(output, frame_plot) #matplotlib 2.2版本之后推荐使用NavigationToolbar2Tk，若使用NavigationToolbar2TkAgg会警告
    toolbar.update()
    root.after(1000, dels)
    

    
root.protocol("WM_DELETE_WINDOW",shutdown)
root.mainloop()
