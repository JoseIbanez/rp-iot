#!/usr/bin/env python

import time
import logging
import logging.handlers
import argparse
import sys
import socket
import json
import yaml
import datetime
import re
import mqttClient


def main():
    subList = { "D0": "ESP001D0", 
                "D1": "ESP001D1"}

    myClient = mqttClient.MqttClient(subList,broker="127.0.0.1")


    myClient.send_order("ESP001D0","0000;0000")
    myClient.send_raw("a/ESP001D0","ok")
    myClient.send_raw("a/ESP001D1","ok")

    myClient.send_order("ESP001D1","0000;0000")


    time.sleep(10)

if __name__ == "__main__":
    main()
