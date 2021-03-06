#!/usr/bin/env python


import logging
import logging.handlers
from sys import platform

import json
import boto3
import datetime
import yaml
import re
from optparse import OptionParser


arn = ""
probeId = ""
probeType = ""
probePath = ""

#logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if platform == "linux" or platform == "linux2":
    handler = logging.handlers.SysLogHandler(address="/dev/log")
elif platform == "darwin":
    handler = logging.handlers.SysLogHandler(address="/var/run/syslog")
logger.addHandler(handler)
#logger.debug('this is debug')
#logger.critical('this is critical')


def load_config(configPath):
    global arn
    global probeId
    global probeType
    global probePath


    with open(configPath, 'r') as stream:
        try:
            config = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    probeId = config['id']
    probeType = config['type']
    probePath = config['path']

    #arn = "arn:aws:sns:eu-west-1:532272748741:Teste"
    arn = "arn:aws:sns:eu-west-1:532272748741:temp"

   
    logger.info('Set arn:'+arn)
    logger.info('Set probeId:'+probeId)
    logger.info('Set probeType:'+probeType)

def read_ds18b20(path):
    with open(path, "r") as myfile:
        data = myfile.read()

    temp = None
    m = re.search(r't=(\d+)', data)
    if m:
        logger.info('Temp:'+m.group(0))
        temp = int(m.group(1))

    return temp

def read_oregon(path):
    with open(path, "r") as myfile:
        data = myfile.read()

    temp = None
    m = re.search(r'Temp: ([+-]?\d+)', data)
    if m:
        logger.info('Temp:'+m.group(0))
        temp = int(m.group(1))

    humidity = None
    m = re.search(r'Humidity: (\d+)', data)
    if m:
        logger.info('Humidity:'+m.group(0))
        humidity = int(m.group(1))

    return temp, humidity



def read_linuxTemp(path):
    return 37000

def set_message(temp,humidity):

    #use ISO format for date
    date = datetime.datetime.utcnow().isoformat()+"Z"

    message = {'date': date,
               'probe': probeId,
               'temp': temp
              }

    if humidity:
        message['humidity'] = humidity

    logger.info("Message:"+json.dumps(message))
    return message


def upload(message):


    try:
        client = boto3.client('sns')
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        logger.info("AWS answer"+str(response))

    except Exception as e:
        # handle any exception
        logger.error("AWS SNS error '{0}' occured. Arguments {1}.".format(e.message, e.args))



def main():

    #Get options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="configPath",
                      help="Configuration file",
                      default="./probe.yaml")
    (options, _) = parser.parse_args()

    load_config(options.configPath)

    temp = None
    humidity = None

    if probeType == "Linux":
        temp = read_linuxTemp(probePath)

    if probeType == "DS18B20":
        temp = read_ds18b20(probePath)

    if probeType == "OS":
        temp, humidity = read_oregon(probePath)


    message=set_message(temp,humidity)

    upload(message)

if __name__ == '__main__':
    main()
