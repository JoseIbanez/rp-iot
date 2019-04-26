#!/usr/bin/env python


from gpiozero import DigitalOutputDevice
from time import sleep


rLight = DigitalOutputDevice(21,active_high=False)
rPump = DigitalOutputDevice(20,active_high=False)




rLight.on()
sleep(1)
rLight.off()
sleep(1)
rLight.on()
sleep(1)
rLight.off()
sleep(5)

rLight.on()
rPump.on()

sleep(30)
rPump.off()
sleep(10)
rLight.off()




