#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

#python ./test4.py -port /dev/rfcomm1 -msg "200;0001"
#sleep 200

python ./test4.py -port /dev/rfcomm1 -msg "5;0001"
sleep 6

python ./test4.py -port /dev/rfcomm1 -msg "15;1001"
sleep 10
python ./test4.py -port /dev/rfcomm1 -msg "15;0101"
sleep 10

python ./test4.py -port /dev/rfcomm1 -msg "900;0001"



