# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 19:30:34 2019

@author: Luming & Ian
"""
import os
import pandas as pd
import numpy as np
import serial
import time
from time import sleep
import threading
import sys
import struct
import binascii
import math
from time import gmtime, strftime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
#from quickstart.py import *

cle_datime=[]
data_time=[]
file_list=[]
x=[]
y=[]
z=[]
ttime=[]
count=[]


# the configuration of the serial port 
COM_PORT = 'COM1' 
#BAUD_RATES = 115200
BAUD_RATES = 256000

sampleSec = int(input('get the data time interval(time/s):'))
loopNum = 0

readbyte  = 11000 # Unit in byte # 1000 Hz * 3 axis * 4 byte(float)


while loopNum < sampleSec:
    offsetNum = 9999
    while (offsetNum == 9999):
        try:
            ser = serial.Serial(COM_PORT, BAUD_RATES, timeout=1, stopbits=1, bytesize=8)
            data_bin = ser.read(readbyte + 3) # Unit in byte # Leave 3 bytes to check the offset
            #with open('./raw.bin', 'wb') as fid:
            #    fid.write(data)    
            ser.close()
            #print('Done.')

            '''
            fileName = 'raw.bin'
            with open(fileName, 'rb') as fid:
                data_bin = fid.read()
                print("data size: {} bytes".format(sys.getsizeof(data_bin)))
                print("----------------")
            '''
            
            for ii in range(0,3):
                floatbyte = readbyte // 4
                fmt = str(floatbyte) + "f"
                data_decode = struct.unpack_from(fmt, data_bin, offset = ii) # offset unit: byte # float 4 bytes
                print("the offset of the pointer within the file: {} byte".format(ii))
                logVal = abs(math.log(abs(data_decode[0]), 10)) +\
                         abs(math.log(abs(data_decode[1]), 10)) +\
                         abs(math.log(abs(data_decode[2]), 10))        

                if logVal < 5:
                    offsetNum = ii
                    print(data_decode[0:3])
                    print("log value: {}".format(logVal))
                    print("offset: {}".format(offsetNum))
                    print("----------------")
                    break

                print(data_decode[0:3])
                print("log value: {}".format(logVal))
                print("offset: {}".format(offsetNum))
                print("----------------")
        except:
            print('Failed to open the port.')

    data_decode = struct.unpack_from(fmt, data_bin, offset = offsetNum)
    data_decode = list(data_decode)

    if data_decode[0] > 900:
        data_decode = data_decode[1:]
    elif data_decode[1] > 900:
        data_decode = data_decode[2:]

    if (len(data_decode) % 3) > 0:
        lastGroup = len(data_decode) - len(data_decode) % 3
        data_decode = data_decode[:lastGroup]

    now = strftime("%Y%m%d%H%M%S")
    queryFid = "./o_data/{}_{}.bin".format(now, loopNum)
    with open(queryFid, "w") as file:
        file.write(str(data_decode))
    
    print("Done. loop = {}".format(loopNum))
    loopNum += 1
#trans the data form
    
for dirPath, dirNames, fileNames in os.walk("./o_data"):
    print (dirPath)
    for f in fileNames:
        cle_datime.append(f)
        with open('./o_data/'+f,'r') as k:
            aa=k.readlines()
            for i in range(len(aa)):
                file_list.append(aa[i].strip('[]').split(','))
for i in range(len(file_list)):
    for j in range(len(file_list[i])):
        if j % 3 == 0:
            x.append(file_list[i][j])
        elif j % 3 == 1:
            y.append(file_list[i][j])
        else :
            z.append(file_list[i][j])

#deal with the data time
for i in range(len(cle_datime)):
    data_time.append(cle_datime[i].strip('acc3_')[0:14])
    
#transform to the dataframe    

bb=pd.DataFrame()
cc=pd.DataFrame()
cc['time']=time
cc=pd.to_datetime(cc['time'])
bb['time']=cc
bb['x']=x
bb['y']=y
bb['z']=z

bb.to_csv('./upload_code/google-drive-api-tutorial-master/google-drive-upload/AA/'+strftime("%Y%m%d%H%M%S")+'original_data.csv')

