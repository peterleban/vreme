#!/bin/sh

dir=/home/pi/data
date=`date +%Y%m%d`
hour=`date +"%H:%M"`

cd $dir/03/31

/usr/bin/ffmpeg -r 60 -pattern_type glob -i "*.jpg" -c:v libx264 -pix_fmt yuv420p -movflags +faststart $dir/20200331.mp4


