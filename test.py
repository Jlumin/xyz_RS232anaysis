# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 16:55:29 2019

@author: Luming
"""
import serial
import time
from time import sleep
import threading
import sys
import struct
import binascii
  
COM_PORT = 'COM1'  # 請自行修改序列埠名稱
BAUD_RATES = 256000
try:
    ser = serial.Serial(COM_PORT, BAUD_RATES,timeout=1,stopbits=1,bytesize=8)
except:
    print('already open')
#print(ser.readline())
#header = ser.read(0)
#data=ser.readlines()
with open('./raw.bin', 'wb') as f:
    ser.write(f.write(ser.read(100000)))
    print(ser.read(100000))
# =============================================================================
# time.sleep(5)
with open('./raw.bin', 'rb') as fin:
    global bina
    data_str1 = fin.read(100000)
    bina = data_str1
    global aa
    aa=len(data_str1)
    global bb
    bb=int(aa/4)
    print(aa)
with open('./raw.bin', 'rb') as aan:
    global c
    c=bb*4
    data_str1 = aan.read(c)
    data_tuple = struct.unpack(str(bb)+'f',data_str1)  #100 4-byte floats
    print(data_tuple)
# =============================================================================
ser.close()