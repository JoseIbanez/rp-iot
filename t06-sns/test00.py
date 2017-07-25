#!/usr/bin/python2.7

import json
import boto3

arn="arn:aws:sns:eu-west-1:532272748741:Teste"

date="20170725T22:10:30Z"
probe="idididid"
temp="22.33"

message = {"foo": "bar",
           'date': date,
           'probe': probe,
           'temp': temp
          }

print json.dumps(message)

#quit

client = boto3.client('sns')
response = client.publish(
    TargetArn=arn,
    Message=json.dumps({'default': json.dumps(message)}),
    MessageStructure='json'
)


