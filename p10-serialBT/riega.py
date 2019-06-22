#!/usr/bin/env python

import time
import serial
import logging
import logging.handlers
import argparse
import sys
import socket
import json
import yaml
import datetime


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
        print("error in file {}".format(tfile))
        maxTemp = 0


    return maxTemp



#
# Send commands
#
def sendCommands(port, cmd):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(port)
    bt = None

    for i in range(10):
        s.send("D0;STATUS")
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
            description='Riega myBalcon')

    parser.add_argument(
            '-config',
            type=str,
            help='config file',
            default="/etc/balcon/riega.yml")

    parser.add_argument(
            '-maxTemp',
            type=int,
            help='testing max. temp., eg. 30')

    parser.add_argument(
            '-currentHour',
            type=int,
            help='testing current hour, eg. 17')


    args = parser.parse_args()


    with open(args.config, 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
        #print config
        timetable = config['timetable']



    maxTemp = getMaxTemp(config['tempFile'])


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
    #print timetable
    for i in range(len(timetable)):

        #print(maxTemp,timetable[i]['temp'],maxTemp >= timetable[i]['temp'])
        #print(currentHour,timetable[i]['hours'], currentHour in timetable[i]['hours'])

        if ((maxTemp >= timetable[i]['temp']) and (currentHour in timetable[i]['hours'])):
            print "Upper for threshold "+str(timetable[i]['temp'])
            print timetable[i]
            cmd = timetable[i]['cmd']
            break



    if not cmd:
        print "Below threshold"
        cmd = config['defaultCmd']

    print "CMD: {}".format(cmd)

    sendCommands(config['port'], cmd)

if __name__ == "__main__":
    main()
