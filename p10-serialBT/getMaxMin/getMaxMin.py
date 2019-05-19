#!/usr/bin/env python
import logging
import boto3
import json
import decimal
from datetime import date, timedelta, datetime
from boto3.dynamodb.conditions import Key, Attr

#logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)



# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def adefault(self, o):
        if isinstance(o, decimal.Decimal):
            #return str(o)
            return int(o)
        return super(DecimalEncoder, self).default(o)


def lambda_handler(event, context):
    logger.info('got event{}'.format(event))

    probe = safeget(event, 'queryStringParameters', 'probe')
    hours = int(safeget(event, 'queryStringParameters', 'hours'))
    param = safeget(event, 'queryStringParameters', 'param')


    logger.info('hours: {}, probe: {}, param: {}'.format( hours, probe, param ))

    ret = getMaxMin(probe=probe, hours=hours, param=param)

    return {
        "statusCode": 200,
        "body": json.dumps(ret)
    }


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct


def getMaxMin(probe="b827eb.300520.c3",hours=48,param="temp"):

    lastDate =    datetime.today() + timedelta(hours=24)
    initialDate = datetime.today() - timedelta(hours=hours)


    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table('temp')


    print("reading last values")
    print("From: "+initialDate.strftime("%Y-%m-%d %H:%M"))
    print("To:   "+lastDate.strftime("%Y-%m-%d %H:%M"))

    response = table.query(
        ProjectionExpression="probe, #date, #temp, humidity, mois, batt",
        ExpressionAttributeNames={"#date": "date", "#temp": "temp"},
        KeyConditionExpression=Key('probe').eq(probe) &
                               Key('date').between(initialDate.strftime("%Y-%m-%d %H:%M"),
                                                   lastDate.strftime("%Y-%m-%d %H:%M"))
    )


    #print(response[u'Items'])
    #print("-------------------------------------")

    maxItem = { param: None}
    minItem = { param: None}

    for i in response[u'Items']:
        #print(json.dumps(i, cls=DecimalEncoder))

        if param in i.keys():

            item = { "date" : i['date'] }

            if param == 'temp' or param == 'humidity':
                value = float(i[param])/1000
            else:
                value = float(i[param])
            
            item[param]=value

            if (maxItem[param] is None or value > maxItem[param]):
                maxItem = item

            if (minItem[param] is None or value < minItem[param]):
                minItem = item




    out = { "probe": probe, "max": maxItem, "min": minItem }

    return out
