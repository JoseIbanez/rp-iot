#!/bin/bash

home="/home/pi/Projects/rp-iot/p07-sns-temp"
cd $home

probes=`ls -1 /etc/rp-iot/probe*.yaml`
for i in $probes; do 
    ./temp.py -c $i
    sleep 10
done
