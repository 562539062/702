import scipy.io as scio 
import multiprocessing

######## 常量 保留 ##########
sumSegment=8 #总分段数
DSig_shape1 = 168 # 未知含义
data_types = ['2D-6A','科研平台','2号']

#用于画图的每一测点的三种类型值的两种需保存值的三种成分的存档名称
pointname=['Peak_average_wave','Peak_average_high','Peak_average_syn','Peak_meaningful_wave','Peak_meaningful_high',
           'Peak_meaningful_syn','Peak_max_wave','Peak_max_high','Peak_max_syn','Valley_average_wave','Valley_average_high',
           'Valley_average_syn','Valley_meaningful_wave','Valley_meaningful_high', 'Valley_meaningful_syn','Valley_max_wave', 
           'Valley_max_high','Valley_max_syn','Full_average_wave','Full_average_high','Full_average_syn','Full_meaningful_wave',
           'Full_meaningful_high','Full_meaningful_syn','Full_max_wave','Full_max_high','Full_max_syn']

#filename代表科学实验平台所使用到信号文件名
filename=['D01(x).str', 'D02(x).str', 'D03(x).str', 'D04(x).str', 'D05(x).str', 'D06(x).str', 'D07(x).str', 'D08(x).str',
          'D09(x).str', 'D10(x).str', 'S01(x).str', 'S01(y).str', 'S01(z).str', 'S02(x).str', 'S02(y).str', 'S02(z).str', 
          'S03(x).str', 'S03(y).str', 'S03(z).str', 'S04(x).str', 'S04(y).str', 'S04(z).str', 'S05(x).str', 'S05(y).str',
          'S05(z).str', 'S06(x).str', 'S06(y).str', 'S06(z).str', 'S07(x).str', 'S07(y).str', 'S07(z).str', 'S08(x).str', 
          'S08(y).str', 'S08(z).str', 'S09(x).str', 'S09(y).str', 'S09(z).str', 'S10(x).str', 'S10(y).str', 'S10(z).str', 
          'S11(x).str', 'S11(y).str', 'S11(z).str', 'S12(x).str', 'S12(y).str', 'S12(z).str', 'S13(x).str', 'S13(y).str', 
          'S13(z).str', 'S14(x).str', 'S14(y).str', 'S14(z).str', 'S15(x).str', 'S15(y).str', 'S15(z).str', 'S16(x).str', 
          'S16(y).str', 'S16(z).str', 'S17(x).str', 'S17(y).str', 'S17(z).str', 'S18(x).str', 'S18(y).str', 'S18(z).str', 
          'S19(x).str', 'S19(y).str', 'S19(z).str', 'S20(x).str', 'S20(y).str', 'S20(z).str', 'S21(x).str', 'S21(y).str', 
          'S21(z).str', 'S22(x).str', 'S22(y).str', 'S22(z).str', 'S23(x).str', 'S23(y).str', 'S23(z).str', 'S24(x).str', 
          'S24(y).str', 'S24(z).str', 'S25(x).str', 'S25(y).str', 'S25(z).str', 'S26(x).str', 'S26(y).str', 'S26(z).str', 
          'S27(x).str', 'S27(y).str', 'S27(z).str', 'S28(x).str', 'S28(y).str', 'S28(z).str', 'S29(x).str', 'S29(y).str', 
          'S29(z).str', 'S30(x).str', 'S30(y).str', 'S30(z).str', 'S31(x).str', 'S31(y).str', 'S31(z).str', 'S32(x).str', 
          'S32(y).str', 'S32(z).str', 'S33(x).str', 'S33(y).str', 'S33(z).str', 'S34(x).str', 'S34(y).str', 'S34(z).str', 
          'S35(x).str', 'S35(y).str', 'S35(z).str', 'S36(x).str', 'S36(y).str', 'S36(z).str', 'S37(x).str', 'S37(y).str', 
          'S37(z).str', 'S38(x).str', 'S38(y).str', 'S38(z).str', 'S39(x).str', 'S39(y).str', 'S39(z).str', 'S40(x).str', 
          'S40(y).str', 'S40(z).str', 'S41(x).str', 'S41(y).str', 'S41(z).str', 'S42(x).str', 'S42(y).str', 'S42(z).str', 
          'S43(x).str', 'S43(y).str', 'S43(z).str', 'S44(x).str', 'S44(y).str', 'S44(z).str', 'A01(x).str', 'A02(x).str', 
          'A03(x).str', 'M01Ax', 'M01Ay', 'M01Az', 'M02Ax', 'M02Ay', 'M02Az', 'M01Yow', 'M01Roll', 'M01Pitch', 'M02Yow', 
          'M02Roll', 'M02Pitch', 'M12Pitch', 'Z01(x).str', 'Z02(1).str', 'Z03(1).str', 'Z03(2).str', 'Z04(x).str', 'Z05(1).str']

#Signame代表科学实验平台所有信号名（不一定全部用到）
Signame=['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10', 'S1X', 'S1Y', 'S1Z', 'S2X', 'S2Y', 'S2Z', 'S3X', 'S3Y',
         'S3Z', 'S4X', 'S4Y', 'S4Z', 'S5X', 'S5Y', 'S5Z', 'S6X', 'S6Y', 'S6Z', 'S7X', 'S7Y', 'S7Z', 'S8X', 'S8Y', 'S8Z', 'S9X',
         'S9Y', 'S9Z', 'S10X', 'S10Y', 'S10Z', 'S11X', 'S11Y', 'S11Z', 'S12X', 'S12Y', 'S12Z', 'S13X', 'S13Y', 'S13Z', 'S14X',
         'S14Y', 'S14Z', 'S15X', 'S15Y', 'S15Z', 'S16X', 'S16Y', 'S16Z', 'S17X', 'S17Y', 'S17Z', 'S18X', 'S18Y', 'S18Z', 'S19X',
         'S19Y', 'S19Z', 'S20X', 'S20Y', 'S20Z', 'S21X', 'S21Y', 'S21Z', 'S22X', 'S22Y', 'S22Z', 'S23X', 'S23Y', 'S23Z', 'S24X',
         'S24Y', 'S24Z', 'S25X', 'S25Y', 'S25Z', 'S26X', 'S26Y', 'S26Z', 'S27X', 'S27Y', 'S27Z', 'S28X', 'S28Y', 'S28Z', 'S29X',
         'S29Y', 'S29Z', 'S30X', 'S30Y', 'S30Z', 'S31X', 'S31Y', 'S31Z', 'S32X', 'S32Y', 'S32Z', 'S33X', 'S33Y', 'S33Z', 'S34X',
         'S34Y', 'S34Z', 'S35X', 'S35Y', 'S35Z', 'S36X', 'S36Y', 'S36Z', 'S37X', 'S37Y', 'S37Z', 'S38X', 'S38Y', 'S38Z', 'S39X', 
         'S39Y', 'S39Z', 'S40X', 'S40Y', 'S40Z', 'S41X', 'S41Y', 'S41Z', 'S42X', 'S42Y', 'S42Z', 'S43X', 'S43Y', 'S43Z', 'S44X',
         'S44Y', 'S44Z', 'A1', 'A2', 'A3', 'M1-X', 'M1-Y', 'M1-Z', 'M2-X', 'M2-Y', 'M2-Z', 'M1-Yaw', 'M1-Roll', 'M1-Pitch', 'M2-Yaw',
         'M2-Roll', 'M2-Pitch', 'M12-Pitch', 'Z1', 'Z2', 'Z31', 'Z32', 'Z4', 'Z5', 'A1-Heave', 'A2-Heave', 'A3-Heave', 'M1-Heave',
         'M1-Sway', 'M1-Surge', 'M2-Heave', 'M2-Sway', 'M2-Surge']

#delname代表部分不会用到的信号名
delname=['M2-X', 'M2-Y', 'M2-Z', 'M2-Yaw', 'M2-Roll', 'M2-Pitch', 'M12-Pitch', 'Z2', 'Z5', 'A1-Heave', 'A2-Heave', 'A3-Heave',
        'M1-Heave', 'M1-Sway', 'M1-Surge', 'M2-Heave', 'M2-Sway', 'M2-Surge']


############## 循环中使用的范围 ##############
# 增加加速度信号换算位移结果
# 提取加速度A1-A3 和M1
JJ=[i for i,x in enumerate(Signame) if x in ['A1-Heave','A2-Heave','A3-Heave','M1-Heave','M1-Sway','M1-Surge']] #由于索引从0开始，所有数值已-1
index_1=[i for i,x in enumerate(Signame) if x in ['A1','A2','A3','M1-Z','M1-X','M1-Y']]
# 分析锚链张力信号
# 采用标准差方法计算三一值分析锚链张力信号
index_2=[i for i, x in enumerate(Signame) if x in ['Z1','Z31','Z32','Z4']]
# 统计分析不规则波信号中峰值、谷值、峰谷值及其特征值
# index_3=list(range(112))+list(range(113,148))+[151,152,153,158,160,161,162]+list(range(164,JJ[-1]+1)) # JJ[-1]+1 python左闭右开，需取到JJ最后一个元素
index_3=[i for i, x in enumerate(Signame) if (x not in delname) and (x not in ['S35X'])]+JJ
# resultA 的索引范围
# indexa=list(range(142,157))+list(range(164,JJ[-1]+1))
indexa=[i for i, x in enumerate(Signame) if x in['A1','A2','A3','M1-X','M1-Y','M1-Z','M2-X','M2-Y','M2-Z','M1-Yaw','M1-Roll','M1-Pitch','M2-Yaw','M2-Roll','M2-Pitch']]+JJ

DSigRange=[i for i, x in enumerate(Signame) if x not in delname]





if __name__=="__main__":
    print(index_3)