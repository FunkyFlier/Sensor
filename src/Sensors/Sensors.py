import Adafruit_GPIO.FT232H as FT232H
import struct
import time

from datetime import datetime
from datetime import timedelta
from math import floor

# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()

# Find the first FT232H device.
ft232h = FT232H.FT232H()



#gyro defines - ST L3G2
READ_GYRO = 0x80
    
L3G_CTRL_REG1 = 0x20
L3G_CTRL_REG2 = 0x21
L3G_CTRL_REG3 = 0x22
L3G_CTRL_REG4 = 0x23
L3G_CTRL_REG5 = 0x24
L3G_OUT_X_L = 0x28
L3G_WHO_AM_I = 0x0F
L3G_I2C_ADDR = 0x69

gyro = FT232H.I2CDevice(ft232h,L3G_I2C_ADDR)

def millis():
   return floor(time.clock() * 1000)
def micros():
    return floor(time.clock() * 1000000)
def nanos():
    return floor(time.clock() * 1000000000)
def ReadGyro():
    gyroByteList = gyro.readList(L3G_OUT_X_L | READ_GYRO, 6)
    gyroIntList = struct.unpack('hhh',gyroByteList[0:6])
    return gyroIntList;
    xGyro = gyroIntList[0]
    yGyro = gyroIntList[1]
    zGyro = gyroIntList[2]
    #print (xGyro,yGyro,zGyro)
    
def GyroInit():
    
    #whoAmI = gyro.readU8(L3G_WHO_AM_I)
    #print format(whoAmI,'02x')
    #print (bin(whoAmI))
    gyro.write8(L3G_CTRL_REG2, 0x00)
    gyro.write8(L3G_CTRL_REG3, 0x00)
    gyro.write8(L3G_CTRL_REG4, 0x20)
    gyro.write8(L3G_CTRL_REG5, 0x02)
    gyro.write8(L3G_CTRL_REG1, 0x8F)

GyroInit()

gyroList = ReadGyro()

xGyro = gyroList[0] * 0.07
yGyro = gyroList[1] * 0.07
zGyro = gyroList[2] * 0.07


print (xGyro,yGyro,zGyro)



























