#!/usr/bin/python
# coding=utf-8
# "DATASHEET": http://cl.ly/ekot
# https://gist.github.com/kadamski/92653913a53baf9dd1a8
from __future__ import print_function
import serial, struct, sys, time, json, os
from datetime import datetime

DEBUG = 0
CMD_MODE = 2
CMD_QUERY_DATA = 4
CMD_DEVICE_ID = 5
CMD_SLEEP = 6
CMD_FIRMWARE = 7
CMD_WORKING_PERIOD = 8
MODE_ACTIVE = 0
MODE_QUERY = 1

ser = serial.Serial()
ser.port = "/dev/ttyUSB0"
ser.baudrate = 9600

ser.open()
ser.flushInput()

byte, data = 0, ""

def dump(d, prefix=''):
    print(prefix + ' '.join(x.encode('hex') for x in d))

def construct_command(cmd, data=[]):
    assert len(data) <= 12
    data += [0,]*(12-len(data))
    checksum = (sum(data)+cmd-2)%256
    ret = "\xaa\xb4" + chr(cmd)
    ret += ''.join(chr(x) for x in data)
    ret += "\xff\xff" + chr(checksum) + "\xab"

    if DEBUG:
        dump(ret, '> ')
    return ret

def process_data(d):
    r = struct.unpack('<HHxxBB', d[2:])
    pm25 = r[0]/10.0
    pm10 = r[1]/10.0
    checksum = sum(ord(v) for v in d[2:8])%256
    return [pm25, pm10]

def process_version(d):
    r = struct.unpack('<BBBHBB', d[3:])
    checksum = sum(ord(v) for v in d[2:8])%256
    print("Y: {}, M: {}, D: {}, ID: {}, CRC={}".format(r[0], r[1], r[2], hex(r[3]), "OK" if (checksum==r[4] and r[5]==0xab) else "NOK"))

def read_response():
    byte = 0
    while byte != "\xaa":
        byte = ser.read(size=1)

    d = ser.read(size=9)

    if DEBUG:
        dump(d, '< ')
    return byte + d

def cmd_set_mode(mode=MODE_QUERY):
    ser.write(construct_command(CMD_MODE, [0x1, mode]))
    read_response()

def cmd_query_data():
    ser.write(construct_command(CMD_QUERY_DATA))
    d = read_response()
    values = []
    if d[1] == "\xc0":
        values = process_data(d)
    return values

def cmd_set_sleep(sleep=1):
    mode = 0 if sleep else 1
    ser.write(construct_command(CMD_SLEEP, [0x1, mode]))
    read_response()

def cmd_set_working_period(period):
    ser.write(construct_command(CMD_WORKING_PERIOD, [0x1, period]))
    read_response()

def cmd_firmware_ver():
    ser.write(construct_command(CMD_FIRMWARE))
    d = read_response()
    process_version(d)

def cmd_set_id(id):
    id_h = (id>>8) % 256
    id_l = id % 256
    ser.write(construct_command(CMD_DEVICE_ID, [0]*10+[id_l, id_h]))
    read_response()

if __name__ == "__main__":
    cmd_set_sleep(0)
    cmd_set_mode(1);
    pm25=[];
    pm10=[];
    pm25avg=0;
    pm10avg=0;
    for t in range(10):
        values = cmd_query_data();
	time.sleep(1)
    for t in range(5):
	values = cmd_query_data();
	pm25.append(values[0]);
	pm10.append(values[1]);
	time.sleep(1)
    pm10avg=sum(pm10) / float(len(pm10));
    pm25avg=sum(pm25) / float(len(pm25));
#    print("PM 2.5: ", pm25avg, " , PM10: ", pm10avg);
    # append new values
    data = {'sensordatavalues':[{'value_type':'SDS_P1','value':str(pm10avg)},{'value_type':'SDS_P2','value':str(pm25avg)}]}

    # save it to temp file, then rename to avoid corrupted data
    with open('aqitemp.json', 'w') as outfile:
        json.dump(data, outfile, indent=None, separators=(',', ':'))
	os.rename('aqitemp.json', '/home/pi/data/aqi.json')
    cmd_set_mode(0);
    cmd_set_sleep()


    now_seconds = datetime.now().strftime('%s')
    filename=datetime.now().strftime("/home/pi/data/AQI_%Y-%m.log")
    aqi=open(filename,"a+")
    aqi.write("%s,%s,%s\n" %(now_seconds,pm25avg,pm10avg))
    aqi.close()

