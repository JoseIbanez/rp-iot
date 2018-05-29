#!/bin/bash

home='/home/pi/Projects/rp-iot/p08-serialBT'

cd $home

python ./test4.py -port /dev/rfcomm0 -msg "120;0011"


