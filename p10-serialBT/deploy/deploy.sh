#!/bin/bash

sudo mkdir -p /var/spool/balcon/pid/

sudo mkdir -p /var/lib/balcon
sudo chmod 775 /var/lib/balcon
sudo chown $USER /var/lib/balcon

sudo mkdir -p /etc/balcon
sudo chmod 775 /etc/balcon
sudo chown $USER /etc/balcon
cp ../config.yml /etc/balcon/riega.yml

