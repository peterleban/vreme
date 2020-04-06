#!/bin/sh

dir=/home/pi/data
width=640
height=480

date=`date +"%Y%m%d_%H%M%S"`
hour=`date +"%H"`
month=`date +"%m"`
hour=`date +"%H"`

mkdir -p $dir/$month

raspistill -w $width -h $height -q 100 -o $dir/temp.jpg
cp $dir/temp.jpg $dir/$month/webcam_$date.jpg

