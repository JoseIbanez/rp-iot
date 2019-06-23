#!/usr/bin/env python

import time
import logging
import logging.handlers
import argparse
import sys
import socket
import json
import yaml
import datetime
import re
import mqttClient

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
def sendCommands(alias, cmd):

    myClient = mqttClient.MqttClient(alias, broker="127.0.0.1")

    for i, val in enumerate(cmd):
        print "cmd" + str(i)+ ": "+val

        match = re.search("(\w+);(\w+);(\w+)",val)
        if match:
            topicA = match.group(1)
            msg = match.group(2)+";"+match.group(3)
        else:
            print "command error"
            continue;
        
        print "Thing: "+alias[topicA] 
        myClient.send_order(alias[topicA],msg)

        time.sleep(1)

    return


def main():
    #Get options
    parser = argparse.ArgumentParser(
            description='Spray myBalcon')

    parser.add_argument(
            '-config',
            type=str,
            help='config file',
            default="/etc/balcon/spray.yml")

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

    sendCommands(config['alias'], cmd)

if __name__ == "__main__":
    main()
