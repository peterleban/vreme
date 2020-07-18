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

*****************************************************************************

 AS3935_spi_arduino.ino

Zadnja verzija Arduino (Nano) skice, ki uporablja SPI. Skica najprej izvede
samodejno kalibracijo, nato nastavi vrednosti:

   noise floor ... vrednost 1 (0-7)
   spike rejection ... vrednost 1 (0-7)
   watchdog threshold ... vrednost 3 (0-7)
   ojačanje ... indoor (indoor/outdoor)

Nato izvede ponovno kalibracijo.

Pravilna nastavitev zgornjih parametrov je ključna za uspešno delovanje
detektorja! Detektor je namreč zelo občutljiv na elektromagnetne motnje
iz okolice.


