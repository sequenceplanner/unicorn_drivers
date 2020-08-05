#!/usr/bin/python3

import time
import serial

def sendCommand(cmd):
    packet = bytearray()
    packet.append(cmd)
    print(packet)
    ser.write(packet)

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=115200,
    timeout = 3
)

#define commands
ACTUATOR_CMD_COAST = 0
ACTUATOR_CMD_UP = 1
ACTUATOR_CMD_DOWN  = 2

INDICATOR_OFF =  0 << 2
INDICATOR_RED =  1 << 2
INDICATOR_BLUE =  2 << 2
INDICATOR_GREEN =  3 << 2
INDICATOR_YELLOW =  4 << 2
INDICATOR_WHITE =  5 << 2

if(ser.isOpen()):
    print("Serial port open")
    time.sleep(2)
    sendCommand(ACTUATOR_CMD_UP | INDICATOR_GREEN)
    time.sleep(5)
    sendCommand(ACTUATOR_CMD_DOWN | INDICATOR_BLUE)

print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')

print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')
print(ser.readline().decode('utf-8'), end = '')

ser.close()
print("Serial port is closed")
