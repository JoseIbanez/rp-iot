#!/bin/bash

sudo service myThing stop


sudo cp ./myThing.service  /etc/systemd/system/
sudo cp ../myThing.py      /usr/local/bin/
sudo cp ../mqttClient.py   /usr/local/bin/
sudo sed -i "s/{{USER}}/$USER/g" /etc/systemd/system/myThing.service 


sudo service myThing stop
sudo service myThing start

sudo tail -f /var/log/syslog | grep myThing
