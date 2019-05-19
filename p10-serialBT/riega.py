#!/usr/bin/env python

import time
import serial
import logging
import logging.handlers
import argparse
import sys
import socket
import json

#Get options
parser = argparse.ArgumentParser(
         description='Send message to serial port')

parser.add_argument(
        '-port',
        type=str,
        help='serial port, eg. /tmp/channel0',
        default="/tmp/channel0")

parser.add_argument(
        '-msg',
        type=str,
        help='message to send, eg. D1;0010;0001',
        default="D1;0010;0001")

parser.add_argument(
        '-wait',
        action='store_true',
        help='wait for 0')

parser.add_argument(
        '-tfile',
        type=str,
        help='temperature file, eg. /var/lib/balcon/28039.json',
        default="/var/lib/balcon/28039.json")


parser.add_argument(
        '-temp',
        type=int,
        help='threshold temp, eg. 30',
        default=30)

args = parser.parse_args()


try:
    with open(args.tfile, 'r') as file:
        strTemp = file.read()

    print strTemp
    temp = json.loads(strTemp)
    print(temp)

    maxTemp = temp['max']['temp']
    print("maxTemp: {}, threshold {}".format(maxTemp,args.temp))

except:
    print("error in file {}".format(args.tfile))
    maxTemp = 0


if maxTemp >= args.temp:
    print "Upper threshold"
    cmd = args.msg
else:
    print "Below threshold"
    cmd = "D1;0005;0001"



print "CMD: {}".format(cmd)
s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
s.connect(args.port)
s.send(cmd)
data = s.recv(1024)
s.close()
print('Received ' + repr(data))
