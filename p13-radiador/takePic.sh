#!/bin/bash


DATE=$(date +"%Y%m%d-%H%M%S")
NAME="img-$DATE.jpg"

./test02.py &
sleep 1

fswebcam -r 1920x1080 /home/pi/Pictures/$NAME
sleep 1

./twitter_upload.py -text "rad" -file /home/pi/Pictures/$NAME

