#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

python ./test3.py
sleep 30
python ./test3.py -port /dev/rfcomm0 -msg "10;0010"
sleep 5
python ./test3.py -port /dev/rfcomm0 -msg "10;0001"
sleep 5
python ./test3.py -port /dev/rfcomm0 -msg "20;0011"
sleep 5
python ./test3.py -port /dev/rfcomm0 -msg "1;0000"


sleep 30
python ./test3.py -port /dev/rfcomm0 -msg "30;0010" -wait
python ./test3.py -port /dev/rfcomm0 -msg "30;0001" -wait
python ./test3.py -port /dev/rfcomm0 -msg "30;0011" -wait



sleep 5
python ./test3.py -port /dev/rfcomm1 -msg "1;0001"



