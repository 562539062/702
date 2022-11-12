# -*- coding: utf-8 -*-
import scipy.io as scio
import os
import numpy as np
import functions as fc

val_path = os.path.join('..','data_val')
repro_path = os.path.join('..','matlab_reproduce/')
path = os.path.join('..','data') #data path
mat_path = os.path.join( path, 'filename20201129.mat')
load_mat = scio.loadmat(mat_path)
ffilename = '20201114040000' # 按顺序获取具体文件夹名称(不允许有其它文件)
pathstr = os.path.join(path, ffilename)  # 文件路径
filename = load_mat['filename']
Sig, Len, Nright, Nerror = fc.loadSignal20201129(filename, pathstr, segment_length = 720000)
names = os.listdir(val_path)
val_data = {}
for i in names:
    val_data[i.split('.mat')[0]]=scio.loadmat(os.path.join(val_path,i))
#dict_keys(['DDSig', 'DSig_after', 'DSig_before', 'Len', 'Nright', 'resultZ', 'Result_Sample', 'Sig', 'temp'])

def check_matlab():
    re_seg3 = os.path.join(repro_path,'Sigment3.mat')
    re_seg3_data = scio.loadmat(re_seg3)
    
    
    ##DDSig
    np.sum(np.abs((re_seg3_data['DDSig']-val_data['DDSig']['DDSig'])))
    #'resultZ', 'temp'
    np.sum(np.abs((re_seg3_data['resultZ']-val_data['resultZ']['resultZ'])))
    np.sum(np.abs((re_seg3_data['temp']-val_data['temp']['temp'])))
    
    re_seg3_2 = os.path.join(repro_path,'Re202011140403.mat')
    re_seg3_data_2 = scio.loadmat(re_seg3_2)
    
    #Sig_Len_Nright
    re_seg3_3 = os.path.join(repro_path,'Sig_Len_Nright.mat')
    re_seg3_data_3 = scio.loadmat(re_seg3_3)
    #len
    np.sum(np.abs((re_seg3_data_3['Len']-val_data['Len']['Len'])))
    
    #foreDSig-Segment3
    re_seg3_4 = os.path.join(repro_path,'foreDSig-Segment3.mat')
    re_seg3_data_4 = scio.loadmat(re_seg3_4)
    
    np.sum(np.abs((re_seg3_data_4['DSig']-val_data['DSig_before']['DSig'])))
    
    #foreDSig-Segment3
    re_seg3_5 = os.path.join(repro_path,'laterDSig-Segment3.mat')
    re_seg3_data_5 = scio.loadmat(re_seg3_5)
    
    np.sum(np.abs((re_seg3_data_5['DSig']-val_data['DSig_after']['DSig'])))
    
    
    #Sig 
    for i in (re_seg3_data_3['Sig']-val_data['Sig']['Sig']):
        if np.sum(i[0])>0.001:
            print('error')
    
    
    #'Result_Sample'
    for i in (re_seg3_data['Result_Sample']-val_data['Result_Sample']['Result_Sample']):
        if np.sum(i[0])>0.001:
            print('error')
    
    
    #'Sig' error caused by 0-padding
    np.sum(np.abs((re_seg3_data['Sig']-val_data['Sig']['Sig'])))
    
    
    #Nright shape error #need squezze
    np.sum(np.abs((re_seg3_data_3['Nright']-val_data['Nright']['Nright'].squeeze())))

def check_python():
    #len
    print(np.sum(np.abs((Len-val_data['Len']['Len'].squeeze()))))
    #Sig
    squeeze_sig = val_data['Sig']['Sig'].squeeze()
    for i in range(len(squeeze_sig)):
        if not i==157:
            if np.sum(squeeze_sig[i].squeeze() - Sig[i])>0.001:
                print('{} error'.format(i))
    #Nright 
    val = list((val_data['Nright']['Nright'].squeeze()-1))
    val.remove(157)
    np.sum(Nright-val)
    