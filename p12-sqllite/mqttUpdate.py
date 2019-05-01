#!/usr/bin/env python 

import paho.mqtt.client as mqtt #import the client1
import time
import datetime
import sqlite3
from sqlite3 import Error
import re
import sys

# create a database connection
database = "./balcon.db"

############

def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    print("message: ",message)
    print("userdata: ",userdata)

    if re.match( r'^r/ESP.*/\w+$', message.topic):
        print("New temp")

        m = re.match( r'^r/(ESP\w+)\.(\w+)/(\w+)$', message.topic)
        sensor    =  m.group(1)
        port      =  m.group(2)
        parameter =  m.group(3)
        print("sensor ", sensor)
        print("port ", port)

        value     =  str(message.payload.decode("utf-8"))
        print("value ", value)

        now       =  datetime.datetime.utcnow().isoformat()+"Z"

        r = (sensor+"."+port, parameter, value, now)
        add_reading(r)

    print("---")


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None



def add_reading(reading):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    print ">add_reading"

    sql = ''' insert or ignore INTO reading (sensorId,nameId,value,datetime)
              VALUES(?,?,?,?); '''

    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute(sql, reading)

    ret = cur.lastrowid
    print "<ok: "+ str(ret)
    sys.stdout.flush()
    return ret



def aws_set_message(probeId,temp,humidity,mois,batt):

    #use ISO format for date
    date = datetime.datetime.utcnow().isoformat()+"Z"

    message = {'date': date,
               'probe': probeId
              }

    if temp:
        message['temp'] = temp

    if humidity:
        message['humidity'] = humidity

    if mois:
        message['mois'] = mois

    if batt:
        message['batt'] = batt



    print "Message:"+json.dumps(message)
    return message



def aws_upload(message):

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
    broker_address="127.0.0.1"

    print "Starting version (v1.0.2)"
    sys.stdout.flush()


    r = ('ESP111', 'Temp', '22.1', '2015-01-02 12:12')
    r_id = add_reading(r)
    print r_id


    print("creating new instance")
    client = mqtt.Client("BBDD Listen") #create new instance

    #attach function to callback
    client.on_message=on_message 
    print("connecting to broker")
    
    #connect to broker
    client.connect(broker_address) 
    
    #start the loop
    client.loop_start() 

    topic = "r/#"
    print("Subscribing to topic",topic)
    client.subscribe(topic)

    print("Publishing message to topic",topic)
    client.publish("ESP01.A0/temp",22)
    time.sleep(1)
    client.publish("ESP01.A1/mois",50)

    # wait
    while (True):
        time.sleep(4) 
        sys.stdout.flush()

    #stop the loop
    client.loop_stop() 




if __name__ == '__main__':
    main()

########################################

