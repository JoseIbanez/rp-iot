import logging
import time
import json
import uuid
import datetime
import boto3

import discover_csv
import lambda_aux


client = boto3.client('iot-data')


########### AUX ###############################

def get_utc_timestamp(seconds=None):
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime(seconds))

def get_uuid():
    return str(uuid.uuid4())


########## IOT-DATA ###########################
def set_thing_state(thingName, property, state):

    payload = json.dumps({'state': { 'desired': { property : state } }})
    logger.info("IOT update: thingName:"+thingName+", payload:"+payload)

    response = client.update_thing_shadow(
        thingName = thingName, 
        payload =  payload
        )

    #logger.info("IOT response: " + str(response))  
    bodyStr=response['payload'].read()
    body = json.loads(bodyStr)
    #logger.info("Body: "+bodyStr)
    logger.info("IOT update, statusCode:"+str(response['ResponseMetadata']['HTTPStatusCode']))
    logger.info("IOT update, state:"+str(body['state']))




def get_thing_state(thingName, property):

    response = client.get_thing_shadow(thingName=thingName)
    
    streamingBody = response["payload"]
    jsonState = json.loads(streamingBody.read())

    #logger.debug("IOT response: " + str(jsonState)) 
    logger.info("IOT reported: "+ str(jsonState["state"]["reported"]))

    ret = jsonState["state"]["reported"][property]
    return ret


def wait_thing_state(thingName, property, desired):

    waitTime=[100, 100, 500, 500, 1000, 1000, 1000]
    for tw in waitTime:

        time.sleep(tw/1000)
        reported = get_thing_state(thingName, property)

        if (desired == reported):
            logger.info("IOT wait, property updated")
            return "200"

    logger.warn("IOT wait, no response")
    return None






################################################
    
# Setup logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):

    logger.info("Received v3 directive!")
    logger.info(json.dumps(event))
    
    if event['directive']['header']['name'] == "Discover":
        logger.info("Discover")
        response = handle_discovery(event)
        
    elif event['directive']['header']['name'] == "ReportState":
        logger.info("ReportState")
        response = handle_report(event)

    else:
        logger.info("Control")
        response = handle_control(event, context)    

    logger.info("response: " + json.dumps(response))  
    return response


def handle_report(request):

    header = request['directive']['header']
    header['name'] = "StateReport"
    endpoint = request['directive']['endpoint']

    thingName = request['directive']['endpoint']['cookie']['key1']
    property =  request['directive']['endpoint']['cookie']['key2']

    iotValue = get_thing_state(thingName, property)

    if iotValue == "on":
        value = "ON"
    else:
        value = "OFF"
        

    context = {
        "properties": [
            {
                "namespace": "Alexa.PowerController",
                "name": "powerState",
                "value": value,
                "timeOfSample": get_utc_timestamp(),
                "uncertaintyInMilliseconds": 500
            }
        ]
    }

    ###

    response = { 
        "context" : context,
        "event" : { 
            "header" : header, 
            "endpoints" : endpoint,
            "payload" : {}
        }
    }

    return response

    
    


def handle_discovery(request):
    
    user_id = lambda_aux.get_user(request["directive"]["payload"]["scope"]["token"])
    myHome = { "user_id": user_id }
    response = discover_csv.handle_discovery(myHome,request)

    return response
 




def handle_control(request, context):
    request_namespace = request["directive"]["header"]["namespace"]
    request_name = request["directive"]["header"]["name"]
    thingName = request["directive"]["endpoint"]["cookie"]["key1"]
    property  = request["directive"]["endpoint"]["cookie"]["key2"]
    
    desired = None
    value = None

    if request_namespace == "Alexa.PowerController":
        if request_name == "TurnOn":
            desired = "on"
            value = "ON"
        else:
            value = "OFF"
            desired = "off"

    elif request_namespace == "Alexa.PowerLevelController":
        if request_name == "SetPowerLevel":
            desired = request["directive"]["payload"]["powerLevel"]
            value = desired
    
    if not desired:
        return None

    set_thing_state(thingName,property,desired)
    if not wait_thing_state(thingName,property,desired):
        return None


    response = {
        "context": {
            "properties": [
                {
                    "namespace": request_namespace,
                    "name": request_name,
                    "value": value,
                    "timeOfSample": get_utc_timestamp(),
                    "uncertaintyInMilliseconds": 500
                }
            ]
        },
        "event": {
            "header": {
                "namespace": "Alexa",
                "name": "Response",
                "payloadVersion": "3",
                "messageId": get_uuid(),
                "correlationToken": request["directive"]["header"]["correlationToken"]
            },
            "endpoint": {
                "scope": request["directive"]["endpoint"]["scope"],
                "endpointId": request["directive"]["endpoint"]["endpointId"]
            },
            "payload": {}
        }
    }
    return response

