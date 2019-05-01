#!/bin/bash

sudo service mqttUpdate stop

sudo mkdir -p /var/spool/balcon/pid
sudo cp mqttUpdate.service /etc/systemd/system/
sudo cp mqttUpdate.py  /usr/local/bin/mqttUpdate.py 

sudo service mqttUpdate stop
sudo service mqttUpdate start

tail -f /var/log/syslog
