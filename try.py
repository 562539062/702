import numpy as np
import scipy.io as scio
import datetime
import os
import pandas as pd
fid=open('../2#/LtData20201230/测点1/1608262597.dat','rb')
a=np.fromfile(fid, np.float32)
np.save('../try.npy',a)
print(os.path.abspath(os.path.join('../2#/LtData20201230','..')))
# aa=np.load('../')
# b=open('../try.npy')
# c=np.fromfile(b,np.float32)
# print(c)


# fid=open('../newdata/20211001000000/A01(x).str','rb')
# a=np.fromfile(fid, np.float32)
# np.save('../try.npy',a)
# print(a)