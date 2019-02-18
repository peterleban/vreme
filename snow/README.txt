*****************************************************************************
 snow_wemos.ino

Edit the file with WiFi SSID and password.
Wemos D1 will connect to your WiFi network and expects the DHCP server
to assign the IP address.
Use Arduino IDE with proper libraries and board manager to compile and
load to Wemos D1. Once upload complete, use a serial console (9,600 bps)
to see the IP address.

When powered up, the Wemos D1 will be set up as a web server providing
the values:

	[distance,duration]

  distance ... roughly calculated distance [cm] to a closest surface/object
  duration ... time required for the trigger signal from TRIG pin to
               come back to ECHO pin

*****************************************************************************
 readSnow.py

A Python script that runs on a RPi or a PC with python2* version.
This script reads the Wemos D1 values and parses the snow height and duration
values. Optionally, it reads the current temperature (from the weather station)
and compensates for the change in speed of sound.

A script can be run with:

  nohup python readSnow.py &

It goes to background and remains active after the Terminal is closed.

*****************************************************************************
