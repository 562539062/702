import openpyxl
import scipy.io as scio 

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
Rangename=['D1', 'D2','D3','D4','D5','D6','D7','D8','D9','D10','S1X','S1Y','S1Z','S2X','S2Y','S2Z','S3X',
'S3Y','S3Z','S4X','S4Y','S4Z','S5X','S5Y','S5Z','S6X','S6Y','S6Z','S7X','S7Y','S7Z','S8X','S8Y','S8Z','S9X',
'S9Y','S9Z','S10X','S10Y','S10Z','S11X','S11Y','S11Z','S12X','S12Y','S12Z','S13X','S13Y','S13Z','S14X','S14Y',
'S14Z','S15X','S15Y','S15Z','S16X','S16Y','S16Z','S17X','S17Y','S17Z','S18X','S18Y','S18Z','S19X','S19Y','S19Z',
'S20X','S20Y','S20Z','S21X','S21Y','S21Z','S22X','S22Y','S22Z','S23X','S23Y','S23Z','S24X','S24Y','S24Z','S25X',
'S25Y','S25Z','S26X','S26Y','S26Z','S27X','S27Y','S27Z','S28X','S28Y','S28Z','S29X','S29Y','S29Z','S30X','S30Y',
'S30Z','S31X','S31Y','S31Z','S32X','S32Y','S32Z','S33X','S33Y','S33Z','S34X','S34Y','S34Z','S35X','S35Y','S35Z',
'S36X','S36Y','S36Z','S37X','S37Y','S37Z','S38X','S38Y','S38Z','S39X','S39Y','S39Z','S40X','S40Y','S40Z','S41X',
'S41Y','S41Z','S42X','S42Y','S42Z','S43X','S43Y','S43Z','S44X','S44Y','S44Z','A1','A2','A3','M1-X','M1-Y','M1-Z',
'M1-Yaw','M1-Roll','M1-Pitch','Z1','Z31','Z32','Z4']
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




