#!/bin/sh

dir=/home/pi/data
width=640
height=480

date=`date +"%Y%m%d_%H%M%S"`
hour=`date +"%H"`
month=`date +"%m"`
hour=`date +"%H"`
space=`df  | grep /dev/root | awk '{print $4}'`

mkdir -p $dir/$month

if [ $space -ge 500000 ]; then
	raspistill -w $width -h $height -q 100 -o $dir/temp.jpg
	cp $dir/temp.jpg $dir/$month/webcam_$date.jpg
else
	echo "Disk skoraj poln."
fi
