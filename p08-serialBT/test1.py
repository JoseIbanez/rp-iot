import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='/dev/rfcomm1',
    baudrate=9600,
    timeout=5)

if ser.isOpen():
    print "isOpen: True"
else:
    print "isOpen: False"

print ser.portstr       # check which port was really used

ser.write("0;0000")
ans = ser.readline()
if ans == "0000":
   print "Test port: OK"
else:
   print "Test port: Failed"


ser.write("10;1100")      # write a string
ans = ser.readline()


print ans
ser.close()

