import numpy as np
import matplotlib.pyplot as plt


def exp_handle(Sig,index,delta):
    std=[] #标准差
    # avg=[] #平均值
    zt=[] #正太分布
    res=[]
    anw=[]
    #X=[i for i in range(0,int(len(Sig[0])))]
    # 去平 只考虑平的情况所以分段越多越好 按照1000分段 太小影响效率且没意义
    for i in range(0, int(len(Sig) / 1000)):
        t=i*1000
        x=[j for j in range(t,t+1000)]
        y=Sig[t:t+1000]
        stdi=np.std(y)
        if not stdi==0.0:# 保留不是平的信号
            res.extend(y)
        std.append(stdi)
    for i in range(0, int(len(res) / index)):
        t=i*index
        x=[j for j in range(t,t+index)]
        y=res[t:t+index]
        stdi=np.std(y)
        avgi=sum(y)/len(y)
        for j in range(0,len(y)):
            zti=(y[j]-avgi)/stdi
            if zti<delta and zti>(-1*delta):
                zt.append(zti)
                anw.append(y[j])
    return anw





def handle(name,index,delta,n,segment):
    # 读取文件 之后可以用load函数代替 目前是单次处理
    Sig = []
    # name = '../data/A1(X).str'
    padding = True
    fid = open(name, 'rb')
    temp = np.fromfile(fid, np.float32)[1:]
    if segment - len(temp) > 0 and padding == True:
        Sig.append(
            np.concatenate([temp.squeeze(), np.zeros(segment - len(temp))], 0))  # squeeze删除维度1 concatenate合并数组
    else:
        Sig.append(temp.squeeze())
    Sig = Sig[0]
    # first = len(Sig)
    res = []
    # std = []
    for i in range(0, int(len(Sig) / 3000)):
        t = i * 3000
        x = [j for j in range(t, t + 3000)]
        y = Sig[t:t + 3000]
        stdi = np.std(y)
        if not stdi == 0.0:  # 保留不是平的信号
            res.extend(y)
        # 3000分段 每一段原始图像及其标准差
    for i in range(n):
        Sig = exp_handle(Sig, index, delta)

   
    anwx = [i for i in range(1, len(Sig) + 1)]
    # plt.plot(anwx, Sig)
    
    plt.ylim(-20, 20)
    return [anwx, Sig]
    # plt.show()

