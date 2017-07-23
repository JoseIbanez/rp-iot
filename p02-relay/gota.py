#!/usr/bin/python2.7

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)

GPIO.output(17,GPIO.HIGH)
time.sleep(1)


GPIO.output(17,GPIO.LOW)
time.sleep(40)
GPIO.output(17,GPIO.HIGH)

