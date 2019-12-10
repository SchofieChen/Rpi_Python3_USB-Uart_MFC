import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import random
import time



#server = modbus_tcp.TcpServer(address=hostname, port=int(port))
##server.start()
#print('slave server start..')
#tempSlave = server.add_slave(int(1))
#powerSlave = server.add_slave(int(2))
#currentSlave = server.add_slave(int(3))
#tempSlave.add_block('0',cst.HOLDING_REGISTERS,0,16)
#powerSlave.add_block('0',cst.HOLDING_REGISTERS,0,16)
#currentSlave.add_block('0',cst.HOLDING_REGISTERS,0,16)

#while True:
 #   val= 3
  #  tempSlave.set_values('0',3,1)
   # powerSlave.set_values('0',1,2)
    #currentSlave.set_values('0',1,3)
    #time.sleep(0.05)
    #print('set')

class ModbusServer():
    def __init__(self,hostName,port):
        self.hostName = hostName
        self.port = port
        self.slaveID = None
        self.server = None
    
    def startTcpListener(self,):
        server = modbus_tcp.TcpServer(address=self.hostName, port=int(self.port))
        server.start()
        self.server = server 
    
    def addModbusSlave(self,wantedSlaveId):
        newSlave = self.server.add_slave(int(wantedSlaveId))
        newSlave.add_block('0',cst.HOLDING_REGISTERS,0,16)
        return newSlave
        
    def setModbusValue(self, slaveInstance,index,value):
        slaveInstance.set_values('0',index,value)
        
#hostname="192.168.1.2"
#port = 502

#mdbServer = ModbusServer(hostname,port)
#mdbServer.startTcpListener()
#tempslave = mdbServer.addModbusSlave(1)
#mdbServer.setModbusValue(tempslave,1,1)
        
#while(1):
#    mdbServer.setModbusValue(tempslave,1,1)
#    time.sleep(1)
#    print('set')
        