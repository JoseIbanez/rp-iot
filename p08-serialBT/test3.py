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

parser.add_argument(
        '-wait',
        action='store_true',
        help='wait for 0')


args = parser.parse_args()


#syslog config
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.handlers.SysLogHandler(address="/dev/log")
#handler.formatter = logging.Formatter(fmt="%(name)s %(levelname)s: %(message)s")
#handler.ident = 'SerialTester'
handler.formatter = logging.Formatter(fmt="SerialTester[] %(levelname)s: %(message)s")
logger.addHandler(handler)

logger.info("port: "+str(args.port)+" Testing")

count=3
while True:
    # configure the serial connections
    ser = serial.Serial(
        port=args.port,
        baudrate=9600,
        timeout=1)

    time.sleep(5)
    serStatus=ser.isOpen()
    logger.info("ser.isOpen "+str(serStatus))
    print "isOpen: "+str(serStatus)

    #Just for test
    ser.write("STATUS")
    time.sleep(2)
    ans = ser.readline()
    if len(ans) > 0:
        print "Test port: OK"
        logger.info("port: "+str(ser.portstr)+" Test OK, STATUS:"+ans)
        break

    print "Test port: Failed"
    logger.critical("port: "+str(ser.portstr)+" Test Failed")

    count = count - 1
    if count <= 0:
        logger.fatal("port: "+str(ser.portstr)+" Execution aborted.")
        sys.exit(-1)

    ser.close()
    time.sleep(10)


#Send main command
logger.info("port: "+str(ser.portstr)+" Sending cmd: "+args.msg)
ser.write(args.msg)

count = 100
while True:

    #Wait for answer
    time.sleep(5)
    ans = ser.readline()
    print ans

    if len(ans)>0:
        logger.info("port: "+str(ser.portstr)+" Status: "+ans)

    #No wait
    if not args.wait:
	break

    #Wait for final status
    if ans == "0;0000":
        logger.info("port: "+str(ser.portstr)+" Clear confirmed")
        break


    count = count - 1
    if count <= 0:
        logger.fatal("port: "+str(ser.portstr)+" Timeout for clear, Status "+args.port)
        break

    time.sleep(2)
    ser.write("STATUS")


ser.close()
