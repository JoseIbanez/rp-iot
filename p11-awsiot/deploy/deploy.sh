#!/bin/bash

DIR=mything
FILE=myThing

sudo mkdir -p /var/spool/$DIR/pid/

sudo mkdir -p /var/lib/$DIR
sudo chmod 775 /var/lib/$DIR
sudo chown $USER /var/lib/$DIR

sudo mkdir -p /etc/$DIR
sudo chmod 775 /etc/$DIR
sudo chown $USER /etc/$DIR
sudo cp ../iot-config.yml  /etc/$DIR/iot-config.yml
sudo cp ../cert/*          /etc/$DIR/

# /home/pi/Projects/rp-iot/p10-serialBT/riega.py
#
#
