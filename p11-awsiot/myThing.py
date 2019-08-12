#!/usr/bin/env python
'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging
import time
import json
#import argparse
from os.path import expanduser
import yaml
import socket
#import thread
import sys
import subprocess
import argparse
import re
import mqttClient

globalConfig = {}
deviceShadowHandler = None
myClient = None

# Custom Shadow callback
def customShadowCallback_Delta(payload, responseStatus, token):
    print("++++++++DELTA++++++++++")
    print("Payload: "+ str(payload))
    print("responseStatus: "+str(responseStatus))
    print("token: "+str(token))
    payloadDict = json.loads(payload)
    print("state: " + str(payloadDict["state"]))
    print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")

    try:
        state = payloadDict["state"]
    except:
        print("No property received")
        return

    ansState = controlerMapping(state)
    if not ansState:
        return

    #Report ok
    try:
        JSONPayload = {"state":{"reported": state }}
        print("Reporting: "+str(JSONPayload))
        deviceShadowHandler.shadowUpdate(json.dumps(JSONPayload), None, 5)
    except:
        print("report error")



    #Auto-off
    offState = autoOff(state)
    if len(offState) > 0:
        time.sleep(10)
        JSONPayload = {"state":{"desired": offState }}
        print("Auto-off: "+str(JSONPayload))
        deviceShadowHandler.shadowUpdate(json.dumps(JSONPayload), None, 5)
        time.sleep(1)
        JSONPayload = {"state":{"reported": offState }}
        deviceShadowHandler.shadowUpdate(json.dumps(JSONPayload), None, 5)



def autoOff(reqState):

    retState = {}
    config = globalConfig

    for key in reqState:

        action = config['actions'].get(key)
        if not action:
           return retState

        autoOff = action.get('autoOff')
        if not autoOff:
           return retState

        if reqState[key] == "on" and autoOff:
            retState[key] = "off"

    print("Auto-off length: "+str(len(retState)))
    return retState



def controlerMapping(reqState):

    retState = {}
    config = globalConfig

    for key in reqState:

        #print "config: "+str(config['actions'])
        #print "key: "+key
        action = config['actions'].get(key)
        print str(action)

        if not action:
            print "Command not defined"
            continue

        #request state, only valid for on/off devices
        reqValue = reqState[key]
        cmdType = action.get('type')

        cmd  =  action.get(reqValue)

        if not cmdType or not cmd:
            print "Command format error"
            continue

        ###########################################
        if cmdType == "bash":

            print cmd
            try:
                subprocess.Popen(cmd.split())
                retState[key] = reqState[key]
            except:
                print sys.exc_info()[0]


        ###########################################
        if cmdType == "socket":

            sPath = action.get('socket')
            print cmd + " > " + sPath
            try:
                s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                s.connect(sPath)
                s.send(cmd)
                data = s.recv(1024)
                print "socket data: "+data
                retState[key] = reqState[key]
            except Exception as e:
                print "socket error "+str(e)

            try:
                s.close()
            except:
                pass

        ###########################################
        if cmdType == "mqtt":

            ans = mqttCmd(action, cmd)

            if ans:
                retState[key] = reqState[key]




    print retState
    return retState

#
# mqtt CMD handle
#
def mqttCmd(action, cmd):

    global myClient

    config = globalConfig
    alias = config['mqttLocal']['thingAlias']
    print "thingAlias: "+str(alias)

    #broker = action.get('socket')
    broker = config['mqttLocal']['broker']
    print broker + " > " + cmd
    try:

        match = re.search(r"(\w+);(\w+);(\w+)",cmd)
        if match:
            topicA = match.group(1)
            msg = match.group(2)+";"+match.group(3)
        else:
            print "command error"

        print "Thing: "+alias[topicA]

        if not myClient:
            myClient = mqttClient.MqttClient(alias,broker=broker)
        ans = myClient.send_order(alias[topicA],msg)
        return ans

    except Exception as e:
        print "mqtt error "+str(e)
        return None

#
# Test mqtt cmd
#
def test_mqttCmd():

    key = "spray"
    state = "on"

    config = globalConfig
    action = config['actions'].get(key)
    cmd    = action.get(state)

    mqttCmd(action, cmd)



def awsSubscribe():

    config = globalConfig['aws']
    global deviceShadowHandler

    host = config.get('host')
    rootCAPath = expanduser(config.get('rootCAPath'))
    certificatePath = expanduser(config.get('certificatePath'))
    privateKeyPath = expanduser(config.get('privateKeyPath'))
    thingName = config.get('thingName')
    clientId = config.get('clientId')
    print "clientId: "+clientId
    port = 8883


    # Configure logging
    logger = logging.getLogger("AWSIoTPythonSDK.core")
    #logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    # Init AWSIoTMQTTShadowClient
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient(clientId)
    myAWSIoTMQTTShadowClient.configureEndpoint(host, port)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    # AWSIoTMQTTShadowClient configuration
    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec

    # Connect to AWS IoT
    myAWSIoTMQTTShadowClient.connect()

    # Create a deviceShadow with persistent subscription
    deviceShadowHandler = myAWSIoTMQTTShadowClient.createShadowHandlerWithName(thingName, True)

    # Listen on deltas
    deviceShadowHandler.shadowRegisterDeltaCallback(customShadowCallback_Delta)



def main():
    #Get options

    global globalConfig

    parser = argparse.ArgumentParser(
            description='myThing: my AWS Thing')

    parser.add_argument(
            '-config',
            type=str,
            help='config file',
            default="/etc/mything/iot-config.yml")

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
        print "Config File: "+args.config
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)
        globalConfig = config


    #test_mqttCmd()

    awsSubscribe()

    # Loop forever
    while True:
        time.sleep(1)



if __name__ == "__main__":
    main()
