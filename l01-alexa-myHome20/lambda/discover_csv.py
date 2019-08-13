
myCsv = '''
endpointId,manufacturerName,friendlyName,description,displayCategories,thingId,property
rp3_001_001,Raspberry,Riego,Mi riego del balcon del salon,SWITCH,rp3-001,riego
rp3_001_002,Raspberry,Foco planta,Foco para hacer timelapse a planta,SWITCH,rp3-001,foco
rp3_001_003,Raspberry,Balcon,Leds del balcon del salon,SWITCH,rp3-001,balcon
rp3_001_004,Raspberry,Humificador,Humificador del balcon del salon,SWITCH,rp3-001,spray
'''


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

    for :

        sw = {
            "endpointId": "rp3_001_004",
            "manufacturerName": "Raspberry",
            "friendlyName": "Humificador",
            "description": "Humificador del balcon del salon",
            "displayCategories": [ "SWITCH" ],
            "cookie": {
                "key1": "rp3-001",
                "key2": "spray"
            },
            "capabilities": switchCapabilities
        }


        deviceList


    header = request['directive']['header']
    header['name'] = "Discover.Response"
    

    response = { 
        "event" : { 
            "header" : header, 
            "payload" : {
                "endpoints" : [ deviceList ]
            } 
        }
    }








