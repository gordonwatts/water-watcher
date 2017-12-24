#!/bin/env python

from datetime import datetime
from time import sleep

import RPi.GPIO as GPIO

# Configure for running
GPIO.setmode(GPIO.BOARD)
sensor_1_pin = 7

def rc_time (pin):
	'''Returns the time it takes for a pin to go high'''
	count = 0
  
	#Output on the pin for 
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	sleep(0.1)

	#Change the pin back to input
	GPIO.setup(pin, GPIO.IN)
  
	#Count until the pin goes high
	while (GPIO.input(pin) == GPIO.LOW):
		count += 1

	return count

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        print rc_time(sensor_1_pin)
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
