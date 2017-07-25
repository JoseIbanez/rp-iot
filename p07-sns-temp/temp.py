#!/usr/bin/python2.7

import logging
import json
import boto3
import datetime
import yaml
import re
from optparse import OptionParser


arn=""
probeId=""
probeType=""
probePath=""

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_config(configPath):
    global arn
    global probeId
    global probeType
    global probePath 


    with open(configPath, 'r') as stream:
        try:
            config=yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    probeId=config['id']
    probeType=config['type']
    probePath=config['path']

    arn="arn:aws:sns:eu-west-1:532272748741:Teste"
   
    logger.info('Set arn:'+arn);
    logger.info('Set probeId:'+probeId)
    logger.info('Set probeType:'+probeType)

def read_ds18b20(path):
    with open (path, "r") as myfile:
        data=myfile.read()

    temp=None
    m=re.search('t=(\d+)',data)
    if m:
        logger.info('Temp:'+m.group(0));
        temp=int(m.group(1))

    return temp

def read_linuxTemp(path):
    return 37000

def set_message(temp,humidity):

    #use ISO format for date 
    date=datetime.datetime.utcnow().isoformat()+"Z"

    message = {'date': date,
               'probe': probeId,
               'temp': temp
              }

    if humidity:
        print "hola"          

    logger.info("Message:"+json.dumps(message))
    return message


def upload(message):
    client = boto3.client('sns')
    response = client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    logger.info("AWS answer"+str(response))



def main():

    #Get options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="configPath",
                      help="Configuration file",
                      default="./probe.yaml")
    (options, _) = parser.parse_args()

    load_config(options.configPath)
    
    temp=None
    humidity=None

    if probeType == "Linux":
        temp=read_linuxTemp(probePath)

    if probeType == "DS18B20":
        temp=read_ds18b20(probePath)

    message=set_message(temp,humidity)

    upload(message)

if __name__ == '__main__':
    main()