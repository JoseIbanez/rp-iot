#!/usr/bin/env python

import time
import serial
import logging
import logging.handlers
import argparse
import sys
import socket
import json
import datetime

timetable = [
    {
        "temp": 25,
        "hours": [19],
        "cmd": [ "D1;010;0001", "D1;0015;0001", "D1;0015;0001", "D1;0300;0001" ]
    },
    {
        "temp": 30,
        "hours": [23, 02],
        "cmd": [ "D1;010;0001", "D1;0015;0001", "D1;0015;0001", "D1;0300;0001" ]
    }
]




#
# getMaxTemp function
#
def getMaxTemp(tfile):

    # Get max temp for today
    try:
        with open(tfile, 'r') as file:
            strTemp = file.read()

        #print strTemp
        temp = json.loads(strTemp)
        #print(temp)

        maxTemp = temp['max']['temp']
        print("today maxTemp(real): {}".format(maxTemp))

    except:
        print("error in file {}".format(args.tfile))
        maxTemp = 0


    return maxTemp



#
# Send commands
#
def sendCommands(port, cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(args.port)
    bt = None

    for i in range(10):
        s.send("D1;STATUS")
        data = s.recv(1024)
        print('Received ' + data)

        if data == "serStatus2":
            bt = 1
            break

        time.sleep(5)


    # no answer from BT
    if not bt:
        print "BT if down"
        s.close()
        return


    print "BT is up"

    for i, val in enumerate(cmd):
        print "cmd" + str(i)
        s.send(val)
        data = s.recv(1024)
        print('Received ' + repr(data))
        time.sleep(30)

    s.close()
    return


def main():
    #Get options
    parser = argparse.ArgumentParser(
            description='Send message to serial port')

    parser.add_argument(
            '-port',
            type=str,
            help='serial port, eg. /tmp/channel0',
            default="/tmp/channel0")

    parser.add_argument(
            '-tfile',
            type=str,
            help='temperature file, eg. /var/lib/balcon/28039.json',
            default="/var/lib/balcon/28039.json")


    parser.add_argument(
            '-maxTemp',
            type=int,
            help='testing max. temp., eg. 30')

    parser.add_argument(
            '-currentHour',
            type=int,
            help='testing current hour, eg. 17')


    args = parser.parse_args()



    maxTemp = getMaxTemp(args.tfile)


    # Get current hour
    currentHour = datetime.datetime.now().hour
    print "current hour: "+str(currentHour)

    #Test mode
    if args.maxTemp:
        maxTemp = args.maxTemp
        print "Testing exec, maxTemp =" + str(maxTemp) 

    if args.currentHour:
        currentHour = args.currentHour
        print "Testing exec, currentHour =" + str(currentHour)


    #
    # Search temp and hour in timetable
    #
    cmd = None
    for i in range(len(timetable)):

        if ((maxTemp >= timetable[i]['temp']) and (currentHour in timetable[i]['hours'])):
            print "Upper for threshold "+str(timetable[i]['temp'])
            print timetable[i]
            cmd = timetable[i]['cmd']
            break



    if not cmd:
        print "Below threshold"
        cmd = [ "D1;0001;0001", "D1;0001;0001" ]

    print "CMD: {}".format(cmd)

    sendCommands(args.port, cmd)

if __name__ == "__main__":
    main()