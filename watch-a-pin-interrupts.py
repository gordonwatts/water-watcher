#!/bin/env python
# Watch a single pin, dump output to the screen
# Use interrputs to do the work

from datetime import datetime
import sys
import RPi.GPIO as GPIO
from time import sleep

def rc_time (pin):
	'''Returns the time it takes for a pin to go high (microseconds)'''
	count = 0

	#Output on the pin for
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	sleep(0.1)

	#Change the pin back to input
	GPIO.setup(pin, GPIO.IN)
	p_start = datetime.now()

	GPIO.wait_for_edge(pin, GPIO.RISING)
	p_end = datetime.now()

	# Convert to microseconds and return that
	delta = p_end - p_start
	return delta.seconds*1000000 + delta.microseconds

# watch a single pin and print it out.
def watchpin(pin):
	GPIO.setmode(GPIO.BOARD)
	try:
		while True:
			v = rc_time(pin)
			print "Pin %d took %d microseconds to rise" % (pin, v)

	except KeyboardInterrupt:
		pass
	finally:
		GPIO.cleanup()

if __name__ == '__main__':
	pin = 7
	if len(sys.argv) > 1:
		pin = int(sys.argv[1])
	watchpin(pin)
