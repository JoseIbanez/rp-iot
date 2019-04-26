#!/usr/bin/env python


from gpiozero import DigitalOutputDevice
from time import sleep


rLight = DigitalOutputDevice(21,active_high=False)

#rLight.on()
#sleep(10)
rLight.off()




