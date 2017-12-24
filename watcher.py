#!/bin/env python

from datetime import datetime
from time import sleep

while True:
	n = datetime.now()

	#with open("output.txt", "a") as myfile:
	with open("/var/www/html/index.txt", "a") as myfile:
		myfile.write(str(n) + "\n")

	sleep(60)

