#!/bin/sh

cd /home/pi/water-watcher

sudo -u pi python3 ./push-to-onedrive.py root/Documents/IoT/96Rose/Furnace logs
