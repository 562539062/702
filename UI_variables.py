# including all classes in newUI
# almost every component
from settings import *

class Setting_Values:
    def __init__(self, ) -> None:
        self.SFreq=int(50) # 信号频率
        self.Slen=90000 #每段数据长度
        self.Slen_=720000 # Line 115: 720000应设置为研究所设定值由于数据问题暂定为最大值
        # 转换成升沉
        self.FF=0.01 # 低频极限
        self.forcenum=10 #单向应力数量
        self.F1=0.01 # Hz 慢飘成分起始频率
        self.F2=0.095 # Hz 慢飘成分结束频率，波浪成分起始频率
        self.F3=0.5 # Hz 波浪成分结束频率，信号高频起始频率
        self.F4=7 # Hz 信号高频结束频率
        # self.DSig_shape1 = 168 # DSig 长度 ???#####
        # self.SFreq1=50 # Not needed every where???
    
    def modify(self, list):
        # 传入的list元素是string类型，转换一下
        self.SFreq=int(list[0]) # 信号频率
        self.Slen=int(list[1]) #每段数据长度
        self.Slen_=int(list[2]) # Line 115: 720000应设置为研究所设定值由于数据问题暂定为最大值
        # 转换成升沉
        self.FF=int(list[3]) # 低频极限
        self.forcenum=int(list[4]) #单向应力数量
        self.F1=int(list[5]) # Hz 慢飘成分起始频率
        self.F2=int(list[6]) # Hz 慢飘成分结束频率，波浪成分起始频率
        self.F3=int(list[7]) # Hz 波浪成分结束频率，信号高频起始频率
        self.F4=int(list[8]) # Hz 信号高频结束频率