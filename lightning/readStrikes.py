#!/usr/bin/env python
from RPi_AS3935 import RPi_AS3935

import RPi.GPIO as GPIO
import time
from datetime import datetime

GPIO.setmode(GPIO.BCM)

# Rev. 1 Raspberry Pis should leave bus set at 0, while rev. 2 Pis should set
# bus equal to 1. The address should be changed to match the address of the
# sensor. (Common implementations are in README.md)
sensor = RPi_AS3935(address=0x03, bus=0)

sensor.reset()
#sensor.set_indoors(True)
sensor.set_indoors(False)
sensor.set_noise_floor(0)

# Use the capacitance value from the sensor! For the example case, this is
# 0x0B (88 pF). It is set in 8 nF steps (16 steps, B hex = 11 dec)
sensor.calibrate(tun_cap=0x0B)


def handle_interrupt(channel):
    time.sleep(0.003)
    global sensor
    reason = sensor.get_interrupt()
    if reason == 0x01:
        print "Noise level too high - adjusting"
        sensor.raise_noise_floor()
    elif reason == 0x04:
        print "Disturber detected - masking"
        sensor.set_mask_disturber(True)
    elif reason == 0x08:
	# Real lightning
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	now_seconds = datetime.now().strftime('%s')
	now_separated = datetime.now().strftime('%Y,%m,%d,%H,%M,%S')
        distance = sensor.get_distance()
        energy = sensor.get_energy()

        filestrele=datetime.now().strftime("/home/pi/lightning/strele.txt")
        strele=open(filestrele,"a+")
        strele.write("%s,%s\n" %(now,energy))
        strele.close()

        filename=datetime.now().strftime("/home/pi/lightning/data/%Y%m%d_strikes")
        light=open(filename,"a+")
        light.write("%s,%s,%s,%s,%s\n" %(now,energy,distance,now_seconds,now_separated))
        light.close()
	
	jakost="sibko"
	if energy > 25000:
		jakost="zmerno"
	if energy > 50000:
		jakost="mocno"
	if energy > 150000:
		jakost="zelo mocno"

	razdalja=">30 km"
	if distance < 30:
		razdalja="20-30 km"
	if distance < 20:
		razdalja="10-20 km"
	if distance < 10:
		razdalja="5-10 km"
	if distance < 6:
		razdalja="< 5 km"

        filename2=datetime.now().strftime("/home/pi/lightning/data/%Y%m%d_strikes_text")
        light_text=open(filename2,"a+")
        light_text.write("Cas: %s | Jakost: %s\n" % (now,jakost))
        light_text.close()

        filename3=datetime.now().strftime("/home/pi/lightning/last_strike_time.txt")
        last_strike=open(filename3,"w")
        last_strike.write("%s (%s)" % (now,razdalja))
        last_strike.close()


pin = 17

GPIO.setup(pin, GPIO.IN)
GPIO.add_event_detect(pin, GPIO.RISING, callback=handle_interrupt)

print "Waiting for lightning - or at least something that looks like it"

while True:
    time.sleep(0.3)

