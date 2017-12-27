#/bin/sh

find /home/pi/water-watcher/logs/* -mtime 7 -exec rm {} \;

