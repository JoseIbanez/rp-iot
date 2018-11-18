
sudo hcitool scan
sudo hcitool dev

hciconfig hci0 up 
hciconfig

list
agent on
default-agent
pair xx:xx:xx:xx:xx:xx
trust xx:xx:xx:xx:xx:xx

#IBA-R2 00:14:01:03:42:28
#IBA-R3 00:14:03:06:3B:37

devices
paired-devices

sudo rfcomm bind 0 xx:xx:xx:xx:xx:xx
sudo rfcomm release 0

#IBA-R2
sudo rfcomm bind 0 00:14:01:03:42:28

#IBA-R3
sudo rfcomm bind 1 00:14:03:06:3B:37

ls -l /dev/rf*