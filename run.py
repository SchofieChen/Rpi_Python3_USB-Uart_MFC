import serial
import time
import sensorProperty
import sys
import threading
import SensorMdbsServer
from log import MyLog
import configparser
import asyncio


ser = serial.Serial("/dev/ttyUSB0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE,timeout=0.3)
#ser = serial.Serial("/dev/ttyAMA0", 9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE) #for pin out (PIN_8, PIN_10)        
currentCMD = b'\x0207RFD\x0d'

NumberOfMFC = {"01":b'\x0201RFD\x0d',
               "02":b'\x0202RFD\x0d',
               "03":b'\x0203RFD\x0d',
               "04":b'\x0204RFD\x0d',
               "05":b'\x0205RFD\x0d',
               "06":b'\x0206RFD\x0d',
               "07":b'\x0207RFD\x0d',
               "08":b'\x0208RFD\x0d',
               "09":b'\x0209RFD\x0d',
               "10":b'\x0210RFD\x0d',
               "11":b'\x0211RFD\x0d',
               "12":b'\x0212RFD\x0d',
               "13":b'\x0213RFD\x0d',}

class deMFCSensorConstructor():
     def __init__(self,):
        self._sensorValue = 0
        self._currentMappingID = 0
    
     def switchIdentifyNumberAndSetResult(self,SensorValue,currentMappingID):
        self._sensorValue = SensorValue
        try:
            self._currentMappingID = int(currentMappingID) #format is Address
            self._giveValue(sensorInstance,currentMappingID)      
        except:
            mylog.error("error when deconstructor")
            
     def _giveValue(self,sensorInstance,currentMappingID):
        
        try:            
            sensorInstance.slaveID = int(currentMappingID)                      
            sensorInstance.Pressure = self._sensorValue
            print('response from %s'%sensorInstance.slaveID )
            self._setMbusArray2Slave(PressureSlave,sensorInstance.slaveID,sensorInstance.Pressure)
        except:
            mylog.error("error when _giveValue")
            
     def _setMbusArray2Slave(self,mdbsSlaveType,index,Value):
         
         try:
             Value = float(Value)
             Value = int(Value) * 10
             #print(Value)
             index = index -1 #bcz modbus start at 40001 index 0 is 40001, index 1 is 40002
             mdbServer.setModbusValue(mdbsSlaveType,index,Value)
         except:
             mylog.error("error when _setMbusArray2Slave")
             
         

def main():
    dMSC = deMFCSensorConstructor()
    readcount = 10
    try:
        while(1):
            for Dickey in NumberOfMFC:
                currentCMD = NumberOfMFC[Dickey]
                #print(Dickey)
                
                try:
                    ser.write(currentCMD)
                except:
                    ser.close()
                    mylog.error("Error occured when sent RS485 message")
                      
                #time.sleep(0.1)
                #-------------------------------- wait response -----------------------------
                try:
                    recv = ser.read(readcount)#the format is like b'N0' or b'NA'                 
                    recv = recv.decode('ascii') #format is like N0\r or NA\r 
                    recv = recv.split('N')[1].split('\r')[0] #First split to be N0 or NA /**/ 
                                                                #Second split to be 0 or A
                    #print(NumberOfMFC[Dickey])  # Currend Command to which No. device
                    print(recv)                 # deconstruct receive data
                
                    dMSC.switchIdentifyNumberAndSetResult(recv,Dickey)
                        
                except:               
                    #ser.close()
                    mylog.error("Error occured when recive data current command is :%s" %(currentCMD))
                    recv = 999
                    dMSC.switchIdentifyNumberAndSetResult(recv,Dickey)                   
                #-------------------------------- response done -----------------------------
                ser.flushInput()
    except:
        mylog.error("system failed in main")
        sys.exit("system failed in main")
        
if __name__ == '__main__':
    mylog = MyLog()
    try:
        config = configparser.ConfigParser()
        config.read('Config.ini')
        ip = config.get('Internet', 'IPconfig')#GET "Value_ABC"
        print(ip)
    except:
        mylog.error("read config fail")
        
    try:
        sensorInstance = sensorProperty.sensorPropertyInstance() #just one instance bcz sync running 
        MFCSensorCollectionThread = threading.Thread(target = main)
        MFCSensorCollectionThread.start()
        mylog.info("Start MFC-HG200 Sensor")
    except KeyboardInterrupt:
        if ser != None:
            mylog.error("Uart fail")
            ser.close()
    try:
        #hostname="127.0.0.1"
        hostname=ip
        port = 502
        ## initial
        mdbServer = SensorMdbsServer.ModbusServer(hostname,port)
        mdbServer.startTcpListener()
        ## create new slave
        PressureSlave = mdbServer.addModbusSlave(1)
        mylog.info("Start Modbus Server")
    except:
        mylog.error("failed to start Modbus Server")
        
