#!/bin/bash


probes=`ls -1 /etc/rp-iot/probe*.yaml`
for i in $probes; do 
cat $i
sleep 10
done
