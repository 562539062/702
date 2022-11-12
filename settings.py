import openpyxl
import numpy as np
import scipy.io as scio 
import multiprocessing

############### 固定参数 ###############
SFreq1=50 # 信号频率
Slen=90000 #每段数据长度
Slen_=720000 # Line 115: 720000应设置为研究所设定值由于数据问题暂定为最大值
# 转换成升沉
SFreq=int(50)
FF=0.01 # 低频极限
forcenum=10 #单向应力数量
F1=0.01 # Hz 慢飘成分起始频率
F2=0.095 # Hz 慢飘成分结束频率，波浪成分起始频率
F3=0.5 # Hz 波浪成分结束频率，信号高频起始频率
F4=7 # Hz 信号高频结束频率
DSig_shape1 = 168 #
sumSegment=8 #总分段数

#用于画图的每一测点的三种类型值的两种需保存值的三种成分的存档名称
pointname=['Peak_meaningful_wave','Peak_max_wave','Valley_meaningful_wave','Valley_max_wave','Full_meaningful_wave','Full_max_wave',
           'Peak_meaningful_high','Peak_max_high','Valley_meaningful_high','Valley_max_high', 'Full_meaningful_high','Full_max_high',
           'Peak_meaningful_syn','Peak_max_syn','Valley_meaningful_syn','Valley_max_syn','Full_meaningful_syn','Full_max_syn']
load_mat = scio.loadmat('./filename.mat')
#liu: filename file will be updated later
filename = load_mat['filename']
Signame = load_mat['Signame']
#打开记录数据的空白模板
wb=openpyxl.load_workbook('./empty.xlsx')
ws=wb['Sheet1']

############## 循环中使用的范围 ##############
# 增加加速度信号换算位移结果
# 提取加速度A1-A3 和M1
dict_ = {}
for i in range(len(Signame)):
    dict_[Signame[i][0][0]] = i
index_1=[]
for n in ['A1','A2','A3','M1-Z','M1-X','M1-Y']:
    index_1.append(dict_[n])
JJ=[i for i, x in enumerate(Signame) if x in ['A1-Heave','A2-Heave','A3-Heave','M1-Heave','M1-Sway','M1-Surge']] #由于索引从0开始，所有数值已-1
f=open('./DSigRange.txt', encoding='UTF-8')
Rangename=[]
for line in f:
    Rangename.append(eval(line.strip()))
DSigRange=[i for i, x in enumerate(Signame) if x in Rangename]
# 分析锚链张力信号
# 采用标准差方法计算三一值分析锚链张力信号
index_2=[i for i, x in enumerate(Signame) if x in ['Z1','Z31','Z32','Z4']]
# 统计分析不规则波信号中峰值、谷值、峰谷值及其特征值
# index_3=list(range(112))+list(range(113,148))+[151,152,153,158,160,161,162]+list(range(164,JJ[-1]+1)) # JJ[-1]+1 python左闭右开，需取到JJ最后一个元素
index_3=[i for i, x in enumerate(Signame) if (x in Rangename) and (x not in ['S35X'])]+JJ
# resultA 的索引范围
# indexa=list(range(142,157))+list(range(164,JJ[-1]+1))
indexa=[i for i, x in enumerate(Signame) if x in['A1','A2','A3','M1-X','M1-Y','M1-Z','M2-X','M2-Y','M2-Z','M1-Yaw','M1-Roll','M1-Pitch','M2-Yaw','M2-Roll','M2-Pitch']]+JJ
# print(indexa)




