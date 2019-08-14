
import csv



def handle_discovery(request):
    
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

    with open('endpoints.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if (line_count == 0):
                #print(str(row))
                line_count = 1
                continue

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

            deviceList.append(sw)

            #print(str(sw))

    


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






