*****************************************************************************
 readAQI.py

A Python script that connects to the SDS011 sensor and reads the PM values.
Data is stored to daily files and also to a .json file that is compatible
with the Weather Display software. Data is read every 3 minutes.

A script can be run with:

  nohup python readAQI.py &

It goes to background and remains active after the Terminal is closed.
*****************************************************************************
