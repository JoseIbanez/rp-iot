#!/bin/bash

sudo cp mqttUpdate.py  /usr/local/bin/mqttUpdate.py 
sudo service mqttUpdate restart
tail -f /var/log/syslog
