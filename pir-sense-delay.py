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
LED1 = 17
LED2 = 27
ENABLE_FLASHING = True

GPIO.setup(PIR, GPIO.IN) #PIR
GPIO.setup(RELAY, GPIO.OUT) #relay
GPIO.setup(LED1, GPIO.OUT)
GPIO.setup(LED2, GPIO.OUT)

GPIO.output(RELAY, False)
GPIO.output(LED1, False)
GPIO.output(LED2, True)


logging.basicConfig(filename='./pir_sense_delay.log',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO)

debug = False
ON_TIME = 60 * 5 # five minutes

BTN_BOUNCETIME = 100

timer = None

def turn_flash_off():
    GPIO.output(LED1, False)

def flash():
    logging.info("flash notification fired")
    # trurn led on
    GPIO.output(LED1, True)
    Timer(0.3, turn_flash_off).start()

def turn_relay_off():
    GPIO.output(RELAY, False)
    GPIO.output(LED2, True)
    logging.info('relay off')
    global timer
    timer = None

def cb(channel):
    logging.info('rising edge on pir')
    # start a timer to call a function to trun off the RELAY
    global timer
    if timer:
        timer.cancel()
        logging.info("delaying: reseting the timer for a new " + str(ON_TIME) + " seconds.")
    else:
        # turn on the RELAY
        logging.info('relay on')
        GPIO.output(RELAY, True)
        GPIO.output(LED2, False)
    # kinda of refresh the timer
    if ENABLE_FLASHING:
        flash()
    timer = Timer(ON_TIME, turn_relay_off)
    timer.start()


GPIO.add_event_detect(PIR, GPIO.RISING, callback=cb, bouncetime=BTN_BOUNCETIME)

try:
	while True:
		time.sleep(60)
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
