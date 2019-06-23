#!/bin/bash

scriptHome=/home/pi/Projects/rp-iot/p10-serialBT
cd $scriptHome
./getMaxMin/test_01.py

scriptHome=/home/pi/Projects/rp-iot/p15-mqtt-spray
cd $scriptHome
./spray.py


