#!/bin/bash

sudo service mqttUpdate stop

sudo cp ./mqttUpdate.service /etc/systemd/system/
sudo cp ../mqttUpdate.py  /usr/local/bin/mqttUpdate.py 
sudo sed -i "s/{{USER}}/$USER/g" /etc/systemd/system/mqttUpdate.service 


sudo service mqttUpdate stop
sudo service mqttUpdate start

sudo tail -f /var/log/syslog
