import time
import serial

# configure the serial connections
ser = serial.Serial(
    port='/dev/rfcomm1',
    baudrate=9600,
    timeout=5)

if ser.isOpen():
    print "isOpen: True"
else:
    print "isOpen: False"

# check which port was really used
print ser.portstr

#Just for test
ser.write("0;0000")
ans = ser.readline()
if ans == "0000":
   print "Test port: OK"
else:
   print "Test port: Failed"


#Main command
ser.write("10;1100")
ans = ser.readline()
print ans


ser.close()

