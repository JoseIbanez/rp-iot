#!/bin/bash

sudo service portServer stop


sudo cp ./portServer.service /etc/systemd/system/
sudo cp ../portServer.py  /usr/local/bin/portServer.py 
sudo sed -i "s/{{USER}}/$USER/g" /etc/systemd/system/portServer.service 


sudo service portServer stop
sudo service portServer start

sudo tail -f /var/log/syslog
