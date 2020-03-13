import serial
import time
##load sensor parameter
import sys
import threading
import asyncio
import os
import multiprocessing as mp
dict = {"01":b'\x0201RPO\x0d',
               "02":b'\x0202RPO\x0d',
               "03":b'\x0203RPO\x0d',
               "04":b'\x0204RPO\x0d',
               "05":b'\x0205RPO\x0d',
               "06":b'\x0206RPO\x0d',
               "07":b'\x0207RPO\x0d',
               "08":b'\x0208RPO\x0d',
               "09":b'\x0209RPO\x0d',
               "10":b'\x0210RPO\x0d',
               "11":b'\x0211RPO\x0d',
               "12":b'\x0212RPO\x0d',
               "13":b'\x0213RPO\x0d',}

list = ["01","02","03","04","05","06","07"
        ,"08","09","10","11","12","13",]

for i in list:
    print(dict[i])

ser = serial.Serial("/dev/ttyUSB0", 115200, serial.EIGHTBITS,
                    serial.PARITY_NONE, serial.STOPBITS_ONE, timeout = 0.1) #for pin out (PIN_8, PIN_10)        
currentCMD = b'\x0207RPO\x0d'
readcount = 10
print(currentCMD)
while(1):
    ser.write(currentCMD)
    print("write")
    recv = ser.read(readcount)#the format is like b'N0' or b'NA'                 
    print(recv)
    if(recv == b''):
        ser.close()
    time.sleep(0.01)
ser.close()
#recv = recv.decode('ascii') #format is like N0\r or NA\r 
#recv = recv.split('N')[1].split('\r')[0] #First split to be N0 or NA /**/ 
                                            #Second split to be 0 or A
#print(NumberOfMFC[Dickey])  # Currend Command to which No. device
#print(recv)                 # deconstruct receive data


