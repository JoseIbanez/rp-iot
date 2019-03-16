#!/bin/bash

PHOME="/home/pi/Projects/rp-iot/radiador"

DATE=$(date +"%Y%m%d-%H%M%S")
NAME="img-$DATE.jpg"

cd $PHOME

rm /home/pi/Pictures/pic.jpg

./tPic.py
mv /home/pi/Pictures/pic.jpg /home/pi/Pictures/$NAME

ls -l /home/pi/Pictures/$NAME

./twitter_upload.py -text "rad" -file /home/pi/Pictures/$NAME

