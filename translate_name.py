import fnmatch
import os
import numpy as np
import datetime 
import shutil
##初始时间1970/01/01 08:00:00+文件名（second）即文件时间
def fun1():
    runpath='../2#/LtData20201230'
    rerunpath='../converted_data'
    Initial_time=datetime.datetime(1970,1,1,8,0,0)
    for file in os.listdir(runpath):
        if fnmatch.fnmatch(file, '测点*'):
            for f in os.listdir(runpath+'/'+file):
                fn=Initial_time+datetime.timedelta(seconds=int(f[:-4]))
                filename=fn.strftime('%Y%m%d%H%M00')
                newpath=rerunpath+'/2#/'+filename
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                shutil.copyfile(runpath+'/'+file+'/'+f,newpath+'/'+file+'.dat')
if __name__=="__main__":
    fun1()
                