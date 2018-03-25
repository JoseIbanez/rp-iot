#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

python ./test4.py -port /dev/rfcomm0 -msg "2;0011"
sleep 10
python ./test4.py -port /dev/rfcomm0 -msg "10;0001"
sleep 10
python ./test4.py -port /dev/rfcomm0 -msg "10;0010"
sleep 10
python ./test4.py -port /dev/rfcomm0 -msg "30;0001"
sleep 30
python ./test4.py -port /dev/rfcomm0 -msg "1;0000"
sleep 5
python ./test4.py -port /dev/rfcomm0 -msg "30;0000"


