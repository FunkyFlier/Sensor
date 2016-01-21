import Adafruit_GPIO.FT232H as FT232H
import struct
import time
import logging

from math import floor
from fileinput import filename

# Temporarily disable FTDI serial drivers.
FT232H.use_FT232H()

# Find the first FT232H device.
ft232h = FT232H.FT232H()


READ = 0x80

#baro defines 
BARO_ADDR                 = 0x76 
MS5611_RESET              = 0x1E
MS5611_PROM_Setup         = 0xA0
MS5611_PROM_C1            = 0xA2
MS5611_PROM_C2            = 0xA4
MS5611_PROM_C3            = 0xA6
MS5611_PROM_C4            = 0xA8
MS5611_PROM_C5            = 0xAA
MS5611_PROM_C6            = 0xAC
MS5611_PROM_CRC           = 0xAE
MS5611_CONVERT_D1_OSR4096 = 0x48   
MS5611_CONVERT_D2_OSR4096 = 0x58   

MS5611_ADC_READ           = 0x00

MS5611_BARO_CONV_TIME     = 50/10^3

#gyro defines - ST L3G2

    
L3G_CTRL_REG1 = 0x20
L3G_CTRL_REG2 = 0x21
L3G_CTRL_REG3 = 0x22
L3G_CTRL_REG4 = 0x23
L3G_CTRL_REG5 = 0x24
L3G_OUT_X_L   = 0x28
L3G_WHO_AM_I  = 0x0F
L3G_I2C_ADDR  = 0x69#0110 1001

#mag defines ST HMC5983DLHC - will work with the HMC5883L
MAG_ADDRESS     = 0x1E  #0001 1110
HMC5983_CRA_REG = 0x00
HMC5983_CRB_REG = 0x01
HMC5983_MR_REG  = 0x02
HMC5983_OUT_X_H = 0x03
HMC5983_OUT_X_L = 0x04
HMC5983_OUT_Z_H = 0x05
HMC5983_OUT_Z_L = 0x06
HMC5983_OUT_Y_H = 0x07
HMC5983_OUT_Y_L = 0x08

HMC5983_ID_A     = 0x0A
HMC5983_ID_B     = 0x0B
HMC5983_ID_C     = 0x0C
HMC5983_WHO_AM_I = 0x0F

#ACC defines
ACC_ADDRESS       = 0x18#0001 1000
CTRL_REG1_A       = 0x20
CTRL_REG2_A       = 0x21
CTRL_REG3_A       = 0x22
CTRL_REG4_A       = 0x23
CTRL_REG5_A       = 0x24
CTRL_REG6_A       = 0x25
HP_FILTER_RESET_A = 0x25
REFERENCE_A       = 0x26
STATUS_REG_A      = 0x27

OUT_X_L_A         = 0x28
OUT_X_H_A         = 0x29
OUT_Y_L_A         = 0x2A
OUT_Y_H_A         = 0x2B
OUT_Z_L_A         = 0x2C
OUT_Z_H_A         = 0x2D

gyro = FT232H.I2CDevice(ft232h,L3G_I2C_ADDR,400000)
mag  = FT232H.I2CDevice(ft232h,MAG_ADDRESS,400000)
acc  = FT232H.I2CDevice(ft232h,ACC_ADDRESS,400000)
baro = FT232H.I2CDevice(ft232h,BARO_ADDR,400000)

testVar = 1.234
testVar1 = 1234
logging.basicConfig(filename='test.log',format='',level=logging.INFO)
# tempString = "%f,%u" %(testVar,testVar1)
# logging.info(tempString)
# logging.info("test")
# logging.info(testVar)
# logging.info(testVar1)
# logging.info("test")

def millis():
    return floor(time.clock() * 1000)
def micros():
    return floor(time.clock() * 1000000)
def nanos():
    return floor(time.clock() * 1000000000)

def BaroReadCoeffs():
    baroIntList = []
    baroByteList = baro.readList(MS5611_PROM_Setup | READ, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
       
    baroByteList = baro.readList(MS5611_PROM_C1, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
          
    baroByteList = baro.readList(MS5611_PROM_C2, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
          
    baroByteList = baro.readList(MS5611_PROM_C3, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
          
    baroByteList = baro.readList(MS5611_PROM_C4, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
          
    baroByteList = baro.readList(MS5611_PROM_C5, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
          
    baroByteList = baro.readList(MS5611_PROM_C6, 2)
    baroIntList.append(struct.unpack('H',baroByteList[0:2])[0])
    #print baroIntList
    return baroIntList

def AccInit():
#     acc.write8(CTRL_REG4_A, 0x00)
#     acc.write8(CTRL_REG1_A, 0x27)
    acc.write8(CTRL_REG1_A, 0x3F)
    acc.write8(CTRL_REG2_A, 0x00)
    acc.write8(CTRL_REG3_A, 0x00)
    acc.write8(CTRL_REG4_A, 0x30)
    acc.write8(CTRL_REG5_A, 0x00)

    
def ReadAcc():
    accByteList = acc.readList(OUT_X_L_A | READ, 6)
    accIntList = struct.unpack('hhh',accByteList[0:6])
    #print accIntList
    return accIntList

def GyroInit():
    #whoAmI = gyro.readU8(L3G_WHO_AM_I)
    #print format(whoAmI,'02x')
    #print (bin(whoAmI))
    gyro.write8(L3G_CTRL_REG2, 0x00)
    gyro.write8(L3G_CTRL_REG3, 0x00)
    gyro.write8(L3G_CTRL_REG4, 0x20)
    gyro.write8(L3G_CTRL_REG5, 0x02)
    gyro.write8(L3G_CTRL_REG1, 0x8F)    
def ReadGyro():
    gyroByteList = gyro.readList(L3G_OUT_X_L | READ, 6)
    gyroIntList = struct.unpack('hhh',gyroByteList[0:6])
    return gyroIntList;


def MagInit():
    #idList = mag.readList(HMC5983_ID_A, 3)
    #print format(idList[0],'02x'),format(idList[1],'02x'),format(idList[2],'02x')
    #print format(mag.readU8(HMC5983_WHO_AM_I),'02x')
    mag.write8(HMC5983_CRA_REG, 0x9C)
    mag.write8(HMC5983_CRB_REG, 0x60)
    mag.write8(HMC5983_MR_REG, 0x80)
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

BaroReadCoeffs()

# 
#    
# GyroInit()
# gyroList = ReadGyro()
    
# MagInit()
# magList = ReadMag()
#   
# AccInit()
# accList = ReadAcc()
#   
# xMag = magList[0]
# yMag = magList[2]
# zMag = magList[1]
#   
# xGyro = gyroList[0] * 0.07
# yGyro = gyroList[1] * 0.07
# zGyro = gyroList[2] * 0.07
#   
# xAcc = accList[0]
# yAcc = accList[1]
# zAcc = accList[2]
#   
#   
# print (xGyro,yGyro,zGyro)
# print (xMag,yMag,zMag)
# print (xAcc,yAcc,zAcc)
#   
# print millis()
# print micros()
# print nanos()
# time = nanos()
#   
# tempString1 = "%i,%f,%f,%f,%i,%i,%i,%i,%i,%i"%(time,xGyro,yGyro,zGyro,xMag,yMag,zMag,xAcc,yAcc,zAcc)
# logging.info(tempString1)
#   
# print ReadMagX()
# print ReadMagY()
# print ReadMagZ()
























