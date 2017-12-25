#!/bin/env python

from datetime import datetime
from time import sleep

import RPi.GPIO as GPIO

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

	def log (self, value):
		''' Log the new pin value'''
		fname = "logs/pin-%d-%s.log" % (self._pin, datetime.strftime(datetime.now(), '%Y-%m-%d'))
		with open(fname, "a") as myfile:
			myfile.write("%s: %d\n" % (datetime.now(), value))

	def update (self):
		'''Monitor pin for a change'''

		# New value and log it
		new_value = rc_time(self._pin)
		self.log (new_value)

		# See if it has changed
		delta = abs(new_value - self._old_value)
		if (delta > self._allowed_delta) or (self._old_value < 0):
			return self.record_state_change(new_value)

		# Allow a moving target.
		if delta > (self._allowed_delta/20):
			self.update_internal_numbers(new_value)
		return None

	def record_state_change(self, new_value):
		# Record info about last state change.
		state_end = datetime.now()
		r = (self._old_value, new_value, state_end - self._state_start, self._pin)
		self._state_start = state_end
		self.update_internal_numbers(new_value)
		return r

	def update_internal_numbers (self, new_value):
		# Update the counters to the new value.
		self._old_value = new_value
		nd = 0.20 * self._old_value
		self._allowed_delta = nd if nd > 500 else 500

# Dump out the text that tells us about the state change
def print_state(info):
	if ((info[2].days != 0) or (info[2].seconds > 1)) or (info[0] < 0):
		mstr = "%s: Pin %d state at level %d (-> %d) lasted %s" % (str(datetime.now()), info[3], info[0], info[1], info[2])
		with open("/var/www/html/index.txt", "a") as myfile:
			myfile.write(mstr + "\n")
		#print mstr

def main ():
	# Pins we should watch
	pins_to_watch = [7, 11]

	# Configure GPIO to run
	GPIO.setmode(GPIO.BOARD)
	# Do our best to clean up if we die
	try:
		# Create the watcher objects
		sensors = [LightSensor(pin) for pin in pins_to_watch]

		while True:
			results = [ls.update() for ls in sensors]
			for v in results:
				if v != None:
					print_state(v)

	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	main()
