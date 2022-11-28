import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from functions import createtimeline
from fnmatch import fnmatch


condidate_values = ['Full_',"Peak_","Valley_", "average_", "meaningful_","max_", "syn","high","wave"]


def generate_value(specific_value, index=0):
    value1 = []
    value2 = []
    value3 = []
    for flag in specific_value[0:3]:
        if flag:
            value1.append(condidate_values[index])
        index += 1
    for flag in specific_value[3:6]:
        if flag:
            value2.append(condidate_values[index])
        index += 1
    for flag in specific_value[6:9]:
        if flag:
            value3.append(condidate_values[index])
        index += 1
    values = []
    for each1 in value1:
        for each2 in value2:
            for each3 in value3:
                values.append(each1 + each2 + each3)
    return values
        


    # if index < len(condidate_values):
    #     if specific_value[index]:
    #         tempValue = tempValue + condidate_values[index]
    #         print('tempValue:'+ tempValue)
    #         return generate_value(specific_value, flag[int(index/3)]+index, tempValue)
    #     else:
    #         flag[int(index/3)] -= 1
    #         return generate_value(specific_value, index+1, tempValue)
    # values.append(tempValue)
    # if flag[int(index/9-1)]:
    #     generate_value(specific_value, flag[int(index/9-1)], '')
    # return tempValue


def plot_tj(signal_name, specific_value, date_start, date_end, dataPath):
    '''整幅图像画在figure.get_figure()上'''
    values = generate_value(specific_value)
    DataPath = dataPath + '/' + signal_name + '/' #'../save/plot_data/S11X/'
    sp=str(date_start)
    ep=str(date_end)
    startdate=sp[0:4]+sp[5:7]+sp[8:]
    enddate=str(int(ep[0:4]+ep[5:7]+ep[8:])+1)
    flag=0
    runfiles=[]
    for f_name in os.listdir(DataPath):
        if fnmatch(f_name, startdate+'*'):
            flag=1
        if flag==1:
            runfiles.append(f_name)
        if fnmatch(f_name, enddate+'*'):
            break
    
    
    time=np.array(createtimeline(runfiles))
    legends = []
    for value in values:
        data = []
        for ffname in runfiles:
            data_path = os.path.join(DataPath + '/' + ffname + '/' + value + '.npy')
            data = np.append(data,np.load(data_path))
        data = np.array(data).flatten()
        plt.plot(time,data)
        legends.append(signal_name + '-' + value)
        print(len(legends))
        plt.legend(legends)
        
        plt.ylabel('Stress Value(MPa)')
        plt.xlabel('Date')
        plt.gca().xaxis.set_major_locator(ticker.AutoLocator())
    # plt.xlim(time.min(),time.max())
    # plt.show()
    
    # plt.cla()
    # plt.clf()
    # plt.close()
    # fig.clear()
    # fig.clf()


# if __name__ == '__main__':
#     plot('S11X',[0, 1, 1, 1, 1, 0, 0, 0, 1],'2015-01-01','2015-02-01','../save/plot_data/')

def plot_Osig(path, segment, padding =True):
    '''padding =True 默认补零'''
    Sig = []
    # name = '../data/A1(X).str'
    fid = open(path, 'rb')
    temp = np.fromfile(fid, np.float32)[1:]
    if segment - len(temp) > 0 and padding == True:
        Sig.append(
            np.concatenate([temp.squeeze(), np.zeros(segment - len(temp))], 0))  # squeeze删除维度1 concatenate合并数组
    else:
        Sig.append(temp.squeeze())
    Sig = np.array(Sig[0])
    x = [i for i in range(1, len(Sig) + 1)]
    return [x,Sig]
    # plt.plot(x, Sig)
    # plt.ylim(-20, -20)
    # plt.ylabel('Stress Value(MPa)')
    # plt.show()


# if __name__=='__main__':
#     fig1 = plt.figure()
#     plot(fig1, 'S13X','Peak_max_wave', 20211001, 20211002, '../save/plot_data')
#     fig2 = plt.figure()
#     plot_Osig(fig2,path='../save/A1(X).str',segment=720000)
    