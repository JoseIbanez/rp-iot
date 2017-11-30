#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

python ./test3.py

sleep 5
python ./test3.py -port /dev/rfcomm0 -msg "1;0001"


sleep 5
python ./test3.py -port /dev/rfcomm1 -msg "1;0001"



