#!/bin/bash

cat  /sys/bus/w1/devices/w1_bus_master1/w1_master_slaves > w1_master_slaves

list=`cat w1_master_slaves`

for i in $list
do 
   cat "/sys/bus/w1/devices/$i/w1_slave" > "$i-w1_slave"
done