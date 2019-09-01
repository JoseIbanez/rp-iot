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



    powerCapabilities = [
        {
            "type": "AlexaInterface",
            "interface": "Alexa.PowerLevelController",
            "version": "3",
            "properties": {
                "supported": [ { "name": "powerLevel" } ],
                "proactivelyReported": True,
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
    
            device = {
                "endpointId": row["endpointId"],
                "manufacturerName": row["manufacturerName"],
                "friendlyName": row["friendlyName"],
                "description": row["description"],
                "cookie": {
                    "key1": row["thingId"],
                    "key2": row["property"]
                }
            }

            if row["displayCategories"] == "SWITCH":
                device["capabilities"] = switchCapabilities
                device["displayCategories"] = [ "SWITCH" ]


            if row["displayCategories"] == "dimmer-SWITCH":
                device["capabilities"] = powerCapabilities
                device["displayCategories"] = [ "SWITCH" ]


            if row["user_id"] == user_id:
                logger.debug("Discover: device:"+row["friendlyName"])
                deviceList.append(device)

            #print(str(device))


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






