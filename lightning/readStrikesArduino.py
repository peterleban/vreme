#!/usr/bin/python
# get lines of text from serial port, save them to a file

from __future__ import print_function

#import RPi.GPIO as GPIO
import time
from datetime import datetime
import serial, io

addr  = '/dev/ttyUSB0'       # serial port to read data from
baud  = 115200               # baud rate for serial port

with serial.Serial(addr,115200) as pt:

    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
        encoding='ascii', errors='ignore', line_buffering=True)
    #spb.readline()  # throw away first line; likely to start mid-sentence (incomplete)
    while (1):
        x = spb.readline()  # read one line of text from serial port
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	now_seconds = datetime.now().strftime('%s') # UNIX timestamp (od 1.1.1970 naprej)
	distance = x.split(",")[0]

        filename=datetime.now().strftime("/home/pi/lightning_arduino/data/%Y%m%d_strikes")
        light=open(filename,"a+")
        light.write("%s,%s,%s" %(now,now_seconds,x))
        light.close()

        filestrele=datetime.now().strftime("/home/pi/lightning_arduino/strele.txt")
        strele=open(filestrele,"a+")
        strele.write("%s,%s" %(now,x))
        strele.close()

	razdalja=">30 km"
	if int(distance) < 30:
		razdalja="20-30 km"
	if int(distance) < 20:
		razdalja="10-20 km"
	if int(distance) < 10:
		razdalja="5-10 km"
	if int(distance) < 6:
		razdalja="< 5 km"

        filename3=datetime.now().strftime("/home/pi/lightning_arduino/last_strike_time.txt")
        last_strike=open(filename3,"w")
        last_strike.write("%s (%s)" % (now,razdalja))
        last_strike.close()
