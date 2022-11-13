import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from functions import createtimeline
from fnmatch import fnmatch
from cProfile import label


def plot(signal_name, specific_value, date_start, date_end, dataPath):
    fig=plt.figure()
    DataPath = dataPath #'../save/plot_data/'
    sp=str(date_start)
    ep=str(date_end)
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
    data = []
    for ffname in runfiles:
        data_path = os.path.join('../save/plot_data/' + signal_name + '/' + ffname + '/' + specific_value + '.npy')
        data.append(np.load(data_path))
    data = np.array(data).flatten()
    time=createtimeline(runfiles)
    # data_path = os.path.join('../save/plot_data/' + signal_name + '/'+ specific_value + '.npy')
    # data=np.load(data_path)
    plt.plot(time,data)
    plt.legend([signal_name + '-' + specific_value])
    plt.gca().xaxis.set_major_locator(ticker.AutoLocator())

    # plt.xlim(time.min(),time.max())


    def mouse_scoll(event):
        current_ax = event.inaxes

        x_min, x_max = current_ax.get_xlim()
        y_min, y_max = current_ax.get_ylim()

        x_step = (x_max-x_min)/10
        y_step = (y_max-y_min)/10

        if event.button == "up":
            current_ax.set(xlim=(x_min+x_step,x_max-x_step),ylim=(y_min+y_step, y_max-y_step))
        elif event.button == "down":
            current_ax.set(xlim=(x_min-x_step,x_max+x_step),ylim=(y_min-y_step, y_max+y_step))
        fig.canvas.draw_idle()


    fig.canvas.mpl_connect('scroll_event', mouse_scoll)

    fig.autofmt_xdate()



    plt.show()