import RPi.GPIO as GPIO 
import time 
GPIO.setmode(GPIO.BCM) 
import logging

GPIO.setup(23, GPIO.IN) #PIR 
GPIO.setup(24, GPIO.OUT) #relay 
logging.basicConfig(filename='/home/pi/projects/pir.log',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.INFO)
	
try:
	time.sleep(2) # to stabilize sensor
	while True:
		if GPIO.input(23):
			logging.info("Motion Detected...")
			# print("detection")
			GPIO.output(24, True)
			time.sleep(5*60) #relay turns on for 3 sec
			GPIO.output(24, False)
			# time.sleep(5) #to avoid multiple detection
		time.sleep(0.3) #loop delay, should be less than detection delay 
except:
    GPIO.cleanup()
