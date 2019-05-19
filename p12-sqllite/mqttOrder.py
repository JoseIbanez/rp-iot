#!/usr/bin/env python 

import paho.mqtt.client as mqtt #import the client1
import time
import datetime
import sqlite3
from sqlite3 import Error
import re
import sys
import json
import boto3
import yaml


thingId = "";
thingAnswer = "";


############

def wait_ok(client, userdata, message):
    global thingAnswer

    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("message: ",message)
    print("userdata: ",userdata)


    if re.match(r'^a/ESP.*$', message.topic):
        print("New msg")
        value     =  str(message.payload.decode("utf-8"))
        print("value ", value)
        thingAnswer = "ok"



    print("---")




def aws_set_message(probeId,param, value):

    #use ISO format for date
    date = datetime.datetime.utcnow().isoformat()+"Z"

    message = {'date': date,
               'probe': probeId
              }

    message[param] = value

    print "Message:"+json.dumps(message)
    return message



def aws_upload(message):

    arn = "arn:aws:sns:eu-west-1:532272748741:temp"

    try:
        client = boto3.client('sns')
        response = client.publish(
            TargetArn=arn,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        print "AWS answer"+str(response)

    except Exception as e:
        # handle any exception
        print "AWS SNS error '{0}' occured. Arguments {1}.".format(e.message, e.args)






def main():
    global thingAnswer
    
    broker_address="192.168.1.19"

    print "Starting version (v0.0.1)"
    sys.stdout.flush()

    thingId = "ESP2C3AE8128E75"

    print("creating new instance")
    client = mqtt.Client("BBDD Listen") #create new instance

    #attach function to callback
    client.on_message=wait_ok 
    print("connecting to broker")
    
    #connect to broker
    client.connect(broker_address) 
    
    #start the loop
    client.loop_start() 

    topic = "a/"+thingId
    print("Subscribing to topic",topic)
    client.subscribe(topic)

    topic = "q/"+thingId
    print("Sending order to thing",topic)
    client.publish("q/"+thingId,"0010;1111")

    time.sleep(2)
    print("ans:"+thingAnswer) 


    #stop the loop
    client.loop_stop() 




if __name__ == '__main__':
    main()

########################################

