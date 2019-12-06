# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 18:14:47 2019

@author: Luming
"""

import serial
import time
from time import sleep
import threading
import sys
import struct
import binascii
import math

COM_PORT = 'COM1'  # 請自行修改序列埠名稱
BAUD_RATES = 256000
# =============================================================================
try:
    ser = serial.Serial(COM_PORT, BAUD_RATES,timeout=1,stopbits=1,bytesize=8)
except:
    print('already open')
aa=input('接收資料:') 
# #print(ser.readline())
#header = ser.read(0)
#data=ser.readlines()
with open('./raw.bin', 'w') as f:
    while aa == 'C':
        bb=time.localtime()
        print(bb)
        data_str1=ser.read(12)
        global aaa
        aaa=len(data_str1)
        global bbb
        bbb=int(aaa/4)
        data_tuple = struct.unpack(str(bbb)+'f',data_str1)
        data_list=list(data_tuple)
#        for i in range(len(data_list)):
#            if abs(math.log10(abs(data_list[i])))< 3:
        f.write(str(time.localtime(time.time()))+str(data_list)+'\n')
        
      
#     print(ser.read(100000))
# =============================================================================
# =============================================================================