#!/usr/bin/env python

import time
import serial
import logging
import logging.handlers
import argparse
import sys

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

count=3
while True:
    # configure the serial connections
    ser = serial.Serial(
        port=args.port,
        baudrate=9600,
        timeout=0.1)

    time.sleep(5)
    serStatus=ser.isOpen()
    logger.info("ser.isOpen "+str(serStatus))
    print "isOpen: "+str(serStatus)

    # check which port was really used
    logger.info("port "+str(ser.portstr))
    print ser.portstr

    #Just for test
    ser.write("0;0000")
    time.sleep(5)
    ans = ser.readline()
    if ans == "0000":
        print "Test port: OK"
        logger.info("Test port: OK")
        break
    
    print "Test port: Failed"
    logger.critical("Test port: Failed")

    count = count - 1
    if count <= 0:
        logger.fatal("Execution aborted")
        sys.exit(-1)

    ser.close()
    time.sleep(10)


#Send main command
logger.info("Sending cmd: "+args.msg)
ser.write(args.msg)

count = 100
while True:

    #Wait for answer
    ans = ser.readline()
    print ans

    if len(ans)>0:
        logger.info("BT answer: "+ans)

    #Wait for final status
    if ans == "0000":
        logger.info("Received confirmation")
        break

    count = count - 1
    if count <= 0:
        logger.fatal("Missing answer")
        break               

    time.sleep(.1)
   
ser.close()