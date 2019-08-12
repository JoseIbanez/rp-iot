#!/bin/bash


ls -l /dev/rfcomm*

if [ ! -c /dev/rfcomm0 ]; then
    echo "rfcomm0 down"
    sudo /usr/bin/rfcomm bind 0 00:14:01:03:42:28
fi

if [ ! -c /dev/rfcomm1 ]; then
    echo "rfcomm1 down"
    sudo /usr/bin/rfcomm bind 1 00:14:03:06:3B:37
fi

echo "now should be up"
ls -l /dev/rfcomm*

