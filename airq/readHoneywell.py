#!/usr/bin/python
import serial
from time import localtime, strftime
import time

port = serial.Serial("/dev/serial0", baudrate=9600, timeout=1.5)
dir = "/home/pi/data/"

if port.isOpen():
    print("Port was opened, closed now.")
    port.close()
port.open()

# Disable Auto Send and verify
port.write(serial.to_bytes([0x68,0x01,0x20,0x77]))
resp = port.read(4)
if ord(resp[0])==165 and ord(resp[1])==165:
    print("Auto Send disabled.")
else:
    print("ERROR: Auto Send NOT disabled.")

# Start the fan and measurements
port.write(serial.to_bytes([0x68,0x01,0x01,0x96]))
resp = port.read(4)
if ord(resp[0])==165 and ord(resp[1])==165:
    print("Fan and measurement started.")
else:
    print("ERROR: Fan and measurement NOT started.")

print("Wait for 10 seconds for fresh air...")

n=0
while (n < 10):
    n+=1
#    print n
    time.sleep(1)

n=0
PM25=[]
PM10=[]

print("  PM2.5    PM10")
print("----------------")
while (n < 10):
    #print("Reading data, attempt %s" % n)
    port.write(serial.to_bytes([0x68,0x01,0x04,0x93]))
    time.sleep(0.5)
    resp = port.read(8);

    if ((65536-(ord(resp[0])+ord(resp[1])+ord(resp[2])+ord(resp[3])+ord(resp[4])+ord(resp[5])+ord(resp[6]))) % 256 )==ord(resp[7]):
        #print("Read successful.")
        PM25.append(ord(resp[3])*256+ord(resp[4]))
        PM10.append(ord(resp[5])*256+ord(resp[6]))
        print("     %s       %s" % (PM25[-1],PM10[-1]))

    else:
        print("ERROR: Reading NOT successful.")
        print(ord(resp[0])+ord(resp[1])+ord(resp[2])+ord(resp[3])+ord(resp[4])+ord(resp[5])+ord(resp[6]))
        print(ord(resp[7]))

    time.sleep(6)
    n+=1

print("----------------")
print("  %.1f      %.1f" %(round(sum(PM25))/len(PM25),round(sum(PM10))/len(PM10) ))


# Stop the fan and measurements
port.write(serial.to_bytes([0x68,0x01,0x02,0x95]))
resp = port.read(4)
if ord(resp[0])==165 and ord(resp[1])==165:
    print("Fan and measurement stopped.")
else:
    print("ERROR: Fan and measurement NOT stopped.")

port.close()
#f.close()

# Open a file to write
#f = open(dir + strftime("%Y-%m-%d", localtime()) + ".txt", "a")
f = open(dir + "aqi.txt", "w")
f.write("%.1f,%.1f" %(round(sum(PM25))/len(PM25),round(sum(PM10))/len(PM10) ))
f.close()
