*****************************************************************************
 readStrikes.py

A Python script that listens to the Franklin sensor connected to the GPIO pins
on the Raspberry Pi.

Default sensitivity is set to "outdoors" meaning it is less sensitive.

	#sensor.set_indoors(True)
	sensor.set_indoors(False)

Capacitance of the sensor is set to 88 pF in this example case. The capacitance
is set in 16 steps by 8 nF. Capacitance information is provided by the sensor
supplier.

A script can be run with:

  nohup python readStrikes.py &

It goes to background and remains active after the Terminal is closed.


*****************************************************************************

 lightning.ino

A source file for Arduino Nano. File is provided by 'Playing With Fusion AS3935
Lightning Sensor'. It is just modified for the output values.

  [distance,energy]


*****************************************************************************
 readStrikesArduino.py

A Python script that listens to the Franklin sensor connected to the USB port
on the Raspberry Pi through Arduino Nano.

A script can be run with:

  nohup python readStrikesArduino.py &

It goes to background and remains active after the Terminal is closed.

