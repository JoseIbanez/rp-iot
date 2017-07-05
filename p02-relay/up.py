#!/usr/bin/python2.7

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
time.sleep(1)

GPIO.output(17,GPIO.HIGH)
GPIO.output(18,GPIO.HIGH)
time.sleep(1)

GPIO.output(18,GPIO.LOW)
time.sleep(1)
GPIO.output(17,GPIO.LOW)
time.sleep(15)

GPIO.output(17,GPIO.HIGH)
GPIO.output(18,GPIO.HIGH)

