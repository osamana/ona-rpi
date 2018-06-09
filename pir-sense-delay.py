#!/usr/bin/python
# script by Osama Abomar
from __future__ import print_function

import RPi.GPIO as GPIO
import time
import subprocess
import signal
import os
import errno
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
import logging
from threading import Timer

PIR = 23
RELAY = 24
LED = 18
ENABLE_FLASHING = False

GPIO.setup(PIR, GPIO.IN) #PIR
GPIO.setup(RELAY, GPIO.OUT) #relay
logging.basicConfig(filename='./pir_sense_delay.log',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO)

debug = False
ON_TIME = 60 * 5 # five minutes

BTN_BOUNCETIME = 50

timer = None

def trun_flash_off():
    GOIO.output(LED, True)

def flash():
    print("Flash")
    # trurn led on
    GOIO.output(LED, True)
    Timer(0.5, turn_flash_off)

def turn_relay_off():
    GPIO.output(RELAY, False)

def cb(channel):
    print('rising edge on pir')
    # turn on the RELAY
    GOIO.output(RELAY, True)
    # start a timer to call a function to trun off the RELAY
    global timer
    if timer:
        timer.cancel()
    # kinda of refresh the timer
    if ENABLE_FLASHING:
        flash()
    timer = Timer(ON_TIME, trun_relay_off)
    timer.start()


GPIO.add_event_detect(PIR, GPIO.RISING, callback=cb, bouncetime=BTN_BOUNCETIME)

try:
	while True:
		time.sleep(60)
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()