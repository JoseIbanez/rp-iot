#!/usr/bin/env python

import time
import serial
import logging
import logging.handlers
import argparse


#Get options
parser = argparse.ArgumentParser(
         description='Send message to serial port')
 
parser.add_argument(
        '-port',
        type=str,
        help='serial port, eg. /dev/rfcomm0',
        default="/dev/rfcomm0")

parser.add_argument(
        '-msg',
        type=str,
        help='message to send, eg. 10;1010',
        default="10;1010")

args = parser.parse_args()


#syslog config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address="/dev/log")
#handler.formatter = logging.Formatter(fmt="%(name)s %(levelname)s: %(message)s")
#handler.ident = 'SerialTester'
handler.formatter = logging.Formatter(fmt="SerialTester[] %(levelname)s: %(message)s")
logger.addHandler(handler)


# configure the serial connections
ser = serial.Serial(
    port=args.port,
    baudrate=9600,
    timeout=5)

serStatus=ser.isOpen()
logger.info("ser.isOpen "+str(serStatus))
print "isOpen: "+str(serStatus)

# check which port was really used
logger.info("porstr "+str(ser.portstr))
print ser.portstr

#Just for test
ser.write("0;0000")
ans = ser.readline()
if ans == "0000":
   print "Test port: OK"
   logger.info("Test port: OK")
else:
   print "Test port: Failed"
   logger.critical("Test port: Failed")


#Main command
ser.write(args.msg)
ans = ser.readline()
print ans
logger.info("BT answer:"+ans)


ser.close()

