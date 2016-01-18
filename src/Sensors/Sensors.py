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


READ = 0x80
#gyro defines - ST L3G2

    
L3G_CTRL_REG1 = 0x20
L3G_CTRL_REG2 = 0x21
L3G_CTRL_REG3 = 0x22
L3G_CTRL_REG4 = 0x23
L3G_CTRL_REG5 = 0x24
L3G_OUT_X_L = 0x28
L3G_WHO_AM_I = 0x0F
L3G_I2C_ADDR = 0x69

#mag defines ST HMC5983DLHC - will work with the HMC5883L
MAG_ADDRESS = 0x1E
HMC5983_CRA_REG = 0x00
HMC5983_CRB_REG = 0x01
HMC5983_MR_REG  = 0x02
HMC5983_OUT_X_H = 0x03
HMC5983_OUT_X_L = 0x04
HMC5983_OUT_Z_H = 0x05
HMC5983_OUT_Z_L = 0x06
HMC5983_OUT_Y_H = 0x07
HMC5983_OUT_Y_L = 0x08

HMC5983_ID_A = 0x0A
HMC5983_ID_B = 0x0B
HMC5983_ID_C = 0x0C
HMC5983_WHO_AM_I = 0x0F

gyro = FT232H.I2CDevice(ft232h,L3G_I2C_ADDR)
mag = FT232H.I2CDevice(ft232h,MAG_ADDRESS)

def millis():
    return floor(time.clock() * 1000)
def micros():
    return floor(time.clock() * 1000000)
def nanos():
    return floor(time.clock() * 1000000000)
def ReadGyro():
    gyroByteList = gyro.readList(L3G_OUT_X_L | READ, 6)
    gyroIntList = struct.unpack('hhh',gyroByteList[0:6])
    return gyroIntList;

def GyroInit():
    #whoAmI = gyro.readU8(L3G_WHO_AM_I)
    #print format(whoAmI,'02x')
    #print (bin(whoAmI))
    gyro.write8(L3G_CTRL_REG2, 0x00)
    gyro.write8(L3G_CTRL_REG3, 0x00)
    gyro.write8(L3G_CTRL_REG4, 0x20)
    gyro.write8(L3G_CTRL_REG5, 0x02)
    gyro.write8(L3G_CTRL_REG1, 0x8F)
    
def ReadMag():
    magByteList = mag.readList(HMC5983_OUT_X_H | READ,6)
    magIntList = struct.unpack('>hhh',magByteList[0:6])
    return magIntList
def ReadMagX():
    magByteList = mag.readList(HMC5983_OUT_X_H | READ,2)
    magIntList = struct.unpack('>h',magByteList[0:2])
    return magIntList
def ReadMagY():
    magByteList = mag.readList(HMC5983_OUT_Y_H | READ,2)
    magIntList = struct.unpack('>h',magByteList[0:2])
    return magIntList
def ReadMagZ():
    magByteList = mag.readList(HMC5983_OUT_Z_H | READ,2)
    magIntList = struct.unpack('>h',magByteList[0:2])
    return magIntList

def MagInit():
    #idList = mag.readList(HMC5983_ID_A, 3)
    #print format(idList[0],'02x'),format(idList[1],'02x'),format(idList[2],'02x')
    #print format(mag.readU8(HMC5983_WHO_AM_I),'02x')
    mag.write8(HMC5983_CRA_REG, 0x9C)
    mag.write8(HMC5983_CRB_REG, 0x60)
    mag.write8(HMC5983_MR_REG, 0x80)



GyroInit()

gyroList = ReadGyro()
MagInit()
magList = ReadMag()

xMag = magList[0]
yMag = magList[2]
zMag = magList[1]

xGyro = gyroList[0] * 0.07
yGyro = gyroList[1] * 0.07
zGyro = gyroList[2] * 0.07


print (xGyro,yGyro,zGyro)
print (xMag,yMag,zMag)

print ReadMagX()
print ReadMagY()
print ReadMagZ()
























