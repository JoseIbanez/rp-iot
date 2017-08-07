#!/bin/bash

home="/home/pi/Projects/rp-iot/p07-sns-temp"
cd $home

find /var/oregonpi/ -type f -mmin +10 -delete
/home/pi/Projects/OregonPi/getTemp /var/oregonpi/os

probes=`ls -1 /etc/rp-iot/oregon*.yaml`
for i in $probes; do 
    ./temp.py -c $i
    sleep 10
done
