#!/usr/bin/python

from __future__ import print_function

import time
from datetime import datetime
import serial, io
import os

addr  = '/dev/ttyUSB0'
baud  = 115200

dir="/home/pi/data"

print("------ Detektor za razelektritve ------")
print("Detektor: AS3935 Playing With Fusion")
print("Delovna mapa: %s" % dir)
print("Serijski port: %s" % addr)
print("Hitrost: %s bps" % baud)
print("---------------------------------------")
print(" Format: cas, epoch, razdalja, energija")
print("|                                     |")

with serial.Serial(addr,baud) as pt:

    spb = io.TextIOWrapper(io.BufferedRWPair(pt,pt,1),
        encoding='ascii', errors='ignore', line_buffering=True)
    while (1):
        x = spb.readline()
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	now_seconds = datetime.now().strftime('%s')
	output = x[0]

	if output == "D":
	    print("Disturber detected: %s" % now)

	if output == "N":
	    print("High noise detected: %s" % now)

	if output == "C":
	    print("Config line: %s" % x.split("C ")[1])

	if output == "S":
	    distance = x.split("S")[1]

	    print("Strike: %s,%s" % (now,distance) )

            filestrele=datetime.now().strftime(dir + "/strele.log")
            strele=open(filestrele,"a+")
            strele.write("%s,%s" %(now,x))
            strele.close()
