import os
import serial
import array
import struct
import datetime

SERIAL_BAUDRATE = 115200
SERIAL_BYTESIZE = serial.EIGHTBITS
SERIAL_PARITY   = serial.PARITY_NONE
SERIAL_STOPBIT  = serial.STOPBITS_ONE
SERIAL_TIMEOUT  = 1

class RS30XController:
    def __init__(self, logging = True):
        self.logging = logging
        self.dev = os.getenv('RS30X_SERIAL_DEVICE')
        self.ser = None
        self.status = {}
        if self.dev is not None:
            self.ser = serial.Serial(self.dev, SERIAL_BAUDRATE, SERIAL_BYTESIZE, SERIAL_PARITY, SERIAL_STOPBIT, SERIAL_TIMEOUT)

    def __send(self, array_obj):
        if self.ser is not None:
            self.ser.flushOutput()
            self.ser.flushInput()
            self.ser.write(array_obj.tostring())
    
    def init(self, id):
        self.initMemMap(id)
        self.torqueOn(id)

    def initMemMap(self, id):
        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x10, 0xFF, 0xFF, 0x00]))
        RS30XController.appendCheckSum(a)
        self.log("initMemMap: %s", a)
        self.__send(a)

    def torqueOn(self, id):
        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x00, 0x24, 0x01, 0x01, 0x01]))
        RS30XController.appendCheckSum(a)
        self.log("torqueOn: %s", a)
        self.__send(a)

    def setReplyDelay(self, id, delay):
        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x60, 0x07, 0x01, 0x01, delay]))
        RS30XController.appendCheckSum(a)
        self.log("setReplyDelay: %s", a)
        self.__send(a)

    def move(self, id, pos, time = None):
        len = 2
        if time is not None:
            len = 4

        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x00, 0x1E, len, 0x01]))
        p = struct.pack('<h',pos)
        u = struct.unpack('<BB',p)
        a.append(u[0])
        a.append(u[1])

        if len > 2:
            t = struct.pack('<h',time)
            u = struct.unpack('<BB',t)
            a.append(u[0])
            a.append(u[1])

        RS30XController.appendCheckSum(a)
        self.log("move: %s", a)
        self.__send(a)

    def getStatus(self, id):
        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x09, 0x00, 0x00, 0x01]))
        RS30XController.appendCheckSum(a)
        self.log("getStatus: %s", a)
        self.__send(a)
        
        p = None
        if self.ser is not None:
            self.log("getStatus: reading...")
            p = self.ser.read(26)
        else:
            p = "\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a"
        self.log("getStatusReply: %s", array.array('B', p))        
        self.status[id] = p[7:25]

    def getPosition(self, id):
        return struct.unpack('<hh', self.status[id][0:4])

    @classmethod
    def createShortPacketHeader(cls, id):
        return array.array('B', [0xFA, 0xAF, id])

    @classmethod
    def appendCheckSum(cls, array_obj):
        sum = array_obj[2]
        for i in range(3, len(array_obj)):
            sum = sum ^ array_obj[i]

        array_obj.extend(array.array('B', [sum])) 

    def log(self, message, *values):
        if self.logging == True:
            print "%s: %s" % (datetime.datetime.now(), message % values)
