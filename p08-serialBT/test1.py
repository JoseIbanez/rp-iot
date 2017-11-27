import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/rfcomm0',
    baudrate=9600)

ser.isOpen()

print ser.portstr       # check which port was really used
ser.write("10;1100")      # write a string
ser.close()  
