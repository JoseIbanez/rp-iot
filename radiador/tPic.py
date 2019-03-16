#!/usr/bin/env python


from gpiozero import DigitalOutputDevice
from time import sleep
from subprocess import call

rLight = DigitalOutputDevice(21,active_high=False)

rLight.on()
sleep(1)

call(["fswebcam", "-r", "1920x1080", "/home/pi/Pictures/pic.jpg"])
sleep(1)

rLight.off()




