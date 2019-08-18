#!/usr/bin/env python


import csv
import logging

# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_discovery(myHome,request):
    
    switchCapabilities = [
        {
            "type": "AlexaInterface",
            "version": "3",
            "interface": "Alexa"
        },
        {
            "type": "AlexaInterface",
            "version": "3",
            "interface": "Alexa.PowerController",
            "properties": {
                "supported": [ { "name": "powerState" } ],
                "retrievable": True
            }
        }
    ]

    deviceList = []

    user_id = myHome["user_id"]
    logger.info("Discover: user_id:"+user_id)


    logger.info("Discover: reading csv file")
    with open('endpoints.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:

            # endpointId,manufacturerName,friendlyName,description,displayCategories,thingId,property
    
            sw = {
                "endpointId": row["endpointId"],
                "manufacturerName": row["manufacturerName"],
                "friendlyName": row["friendlyName"],
                "description": row["description"],
                "displayCategories": [ row["displayCategories"] ],
                "cookie": {
                    "key1": row["thingId"],
                    "key2": row["property"]
                },
                "capabilities": switchCapabilities
            }

            if row["user_id"] == user_id:
                logger.debug("Discover: device:"+row["friendlyName"])
                deviceList.append(sw)

            #print(str(sw))


    logger.info("Discover: Number of devices "+str(len(deviceList)))
    


    header = request['directive']['header']
    header['name'] = "Discover.Response"

    response = { 
        "event" : { 
            "header" : header, 
            "payload" : {
                "endpoints" : deviceList
            } 
        }
    }

    return response






