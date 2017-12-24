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
	p_start = datetime.now()

	#Count until the pin goes high
	while (GPIO.input(pin) == GPIO.LOW):
		count += 1
	p_end = datetime.now()

	# Convert to microseconds and return that
	delta = p_end - p_start
	return delta.seconds*1000000 + delta.microseconds

class LightSensor:
	'''Monitor light sensor bin '''

	def __init__ (self, pin):
		self._pin = pin
		self._old_value = -1
		self._allowed_delta = 500
		self._state_start = datetime.now()

	def update (self):
		'''Monitor pin for a change'''
		new_value = rc_time(self._pin)
		if abs(new_value - self._old_value) > self._allowed_delta:
			return self.record_state_change(new_value)

		# Allow a moving target.
		if abs(new_value - self._old_value) > (self._allowed_delta/10):
			self.update_internal_numbers(new_value)
		return None

	def record_state_change(self, new_value):
		# Record info about last state change.
		state_end = datetime.now()
		r = (self._old_value, new_value, state_end - self._state_start)
		self._state_start = state_end
		self.update_internal_numbers(new_value)
		return r

	def update_internal_numbers (self, new_value):
		# Update the counters to the new value.
		self._old_value = new_value
		nd = 0.25 * self._old_value
		self._allowed_delta = nd if nd > 500 else 500

# Dump out the text that tells us about the state change
def print_state(info):
	if (info[2].days != 0) or (info[2].seconds > 1):
		mstr = "%s: State at level %d lasted %s" % (str(datetime.now()), info[0], info[2])
		#with open("/var/www/html/index.txt", "a") as myfile:
		#	myfile.write(mstr + "\n")
		print mstr

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
	ls1 = LightSensor(sensor_1_pin)

	while True:
		v = ls1.update()
		if v != None:
			print_state(v)

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
