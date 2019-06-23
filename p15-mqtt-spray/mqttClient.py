#!/usr/bin/env python


import re
import time
import paho.mqtt.client as mqtt #import the client1






def wait_ok(client, userdata, message):

    print("message new -------")
    print("message topic= "+ message.topic +", message="+ str(message.payload.decode("utf-8")))
    print("message qos="+ str(message.qos)+ ", retain flag="+ str(message.retain))

    match = re.match(r'^a/(ESP[0-9A-F]+).*$', message.topic)    
    if match:
        print("Answer msg")
        thingId = match.group(1)
        value =  str(message.payload.decode("utf-8"))
        print("thingId:"+thingId+", answer:"+value)
        userdata[thingId]['answer']=value

    print("---")


class MqttClient:

    def __init__(self,subList,broker="192.168.1.19"):
        self.broker=broker
        self.thinkList = {}

        #create new instance    
        print("creating new instance")
        self.client = mqtt.Client("Send Order",userdata=self) 

        #attach function to callback
        self.client.on_message=wait_ok 
        print("connecting to broker")
        
        #connect to broker
        self.client.connect(self.broker) 
        
        #start the loop
        self.client.loop_start() 

        topicList = []
        print("Subcribing to thing list:")
        for id in subList:

            self.thinkList[subList[id]] = { "alias": id,
                                            "id": subList[id],
                                            "answer": "" }

            topicItem = ( "a/"+subList[id], 0 )
            print(topicItem)
            topicList.append(topicItem)

        self.client.subscribe(topicList)




    def send_raw(self,topic,msg): 
        print("Sending order to thing, topic="+topic+", msg="+msg+".")
        self.client.publish(topic,msg)


    def stop(self):
        #stop the loop
        self.client.loop_stop() 


    def send_order(self,thingId,msg):

        topic = "q/"+thingId
        print("Sending order to thing, topic="+topic+", msg="+msg+".")
        self.client.publish(topic,msg)


        time.sleep(2)
        print("topic:"+topic+", ans:"+self.thinkList[thingId]['answer']) 

