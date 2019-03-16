import paho.mqtt.client as mqtt #import the client1
import time
import datetime
import sqlite3
from sqlite3 import Error
import re

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

    if re.match( r'^ESP.*/Temp$', message.topic):
        print("New temp")
        
        m = re.match( r'^(ESP\w+)/(\w+)$', message.topic)
        sensor    =  m.group(1)
        parameter =  m.group(2)
        value     =  str(message.payload.decode("utf-8"))
        now       =  datetime.datetime.now().isoformat()

        r = (sensor, parameter, value, now)
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
    return ret




def main():
    broker_address="127.0.0.1"


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

    topic = "#"
    print("Subscribing to topic",topic)
    client.subscribe(topic)

    print("Publishing message to topic",topic)
    client.publish("ESP01/Temp",22)
    time.sleep(1)
    client.publish("ESP01/humi",50)

    # wait
    #while (True)
    time.sleep(4) 


    #stop the loop
    client.loop_stop() 




if __name__ == '__main__':
    main()

########################################

