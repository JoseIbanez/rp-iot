#!/bin/bash

sudo apt-get install python-pip
sudo pip install awscli boto3

sudo mkdir /var/oregonpi/
sudo chown pi.pi /var/oregonpi/

sudo mkdir /etc/rp-iot/
sudo chown pi.pi /etc/rp-iot/

