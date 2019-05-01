#!/bin/bash

sudo apt-get install -y sqlite3
sudo apt-get install -y python        
sudo apt-get install -y mosquitto mosquitto-clients 
sudo apt-get install -y python-pip
pip install paho-mqtt

sudo mkdir /var/lib/balcon
cp ./balcon.db /var/lib/balcon/

sudo mkdir -p /var/spool/balcon/pid

sudo chown $USER /var/lib/balcon

