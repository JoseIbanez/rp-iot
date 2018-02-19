#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

python ./test4.py -port /dev/rfcomm1 -msg "10;0000"
sllep 5

python ./test4.py -port /dev/rfcomm1 -msg "10;0001"
sleep 5
python ./test4.py -port /dev/rfcomm1 -msg "10;0001"
sleep 5
python ./test4.py -port /dev/rfcomm1 -msg "20;0001"
sleep 5
python ./test4.py -port /dev/rfcomm1 -msg "1;0000"
sleep 5
python ./test4.py -port /dev/rfcomm1 -msg "10;0000"


