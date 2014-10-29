import os
import serial
import array
import struct
import datetime

TTL_SPEED = 115200
TTL_TIMEOUT = 10

class RS30XController:
    def __init__(self):
        self.dev = os.getenv('RS30X_SERIAL_DEVICE')
        self.ser = None
        if self.dev is not None:
            self,ser = serial.Serial(self.dev, TTL_SPEED, TTL_TIMEOUT)

    def __send(self, array_obj):
        if self.ser is not None:
            self.ser.write(array_obj.tostring())

    def initMemMap(self, id):
        a = RS30XController.createShortPacketHeader(id)
        a.extend(array.array('B', [0x10, 0xFF, 0xFF, 0x00]))
        RS30XController.appendCheckSum(a)
        RS30XController.log("initMemMap: %s" % a)
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
        RS30XController.log("move: %s" % a)
        self.__send(a)

    @classmethod
    def createShortPacketHeader(cls, id):
        return array.array('B', [0xFA, 0xAF, id])

    @classmethod
    def appendCheckSum(cls, array_obj):
        sum = array_obj[2]
        for i in range(3, len(array_obj)):
            sum = sum ^ array_obj[i]

        array_obj.extend(array.array('B', [sum])) 


    @classmethod
    def log(cls, message):
        print "%s: %s" % (datetime.datetime.now(), message)
