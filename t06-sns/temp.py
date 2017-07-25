#!/usr/bin/python2.7

import logging
import json
import boto3
import datetime
from optparse import OptionParser


arn=""
probeId=""
probeType=""
probePath=""

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def load_config():
    global arn
    global probeId
    global probeType
    global probePath 

    arn="arn:aws:sns:eu-west-1:532272748741:Teste"
    probeId="idididid"

    logger.info('Set arn:'+arn);
    logger.info('Set probeId:'+probeId)

def read_linux_temp(path):
    return "37.00"

def set_message(temp,humidity):

    #use ISO format for date 
    date=datetime.datetime.utcnow().isoformat()

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

    logger.info("AWS answer"+response)



def main():

    #Get options
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="configPath",
                      help="Configuration file",
                      defult="./probe.conf")
    (options, _) = parser.parse_args()

    load_config(configPath)
    
    if probeType == "Linux":
        temp=read_linux_temp(probePath)
    
    set_message(temp)


if __name__ == '__main__':
    main()