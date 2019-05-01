#!/bin/bash

sudo apt-get install -y sqlite3
sudo apt-get install -y python        
sudo apt-get install -y mosquitto mosquitto-clients 
sudo apt-get install -y python-pip
pip install paho-mqtt

sudo mkdir /var/lib/balcon
sudo chown pi /var/lib/balcon

sudo cp 