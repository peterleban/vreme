#!/bin/sh

DIR=/home/pi/data
width=1067
height=800

HOUR="$(date +'%H')"
  if [ $HOUR -ge 21 ] || [ $HOUR -lt 5 ] ; then
	raspistill -w $width -h $height -q 100 -o $DIR/wcetemp.jpg -ISO 800 -ss 1500000
	convert -pointsize 24 -fill white -annotate +10+50 'Vremenska postaja Tolmin' -annotate +10+80 'kamera S (fisheye)' -annotate +900+50 `date +%d.%m.%Y` -annotate +520+50 `date +%H:%M` $DIR/wcetemp.jpg $DIR/wcef.jpg
  else
	sleep 10
	raspistill -w $width -h $height -q 100 -o $DIR/wcetemp.jpg 
	convert -pointsize 24 -fill black -annotate +10+50 'Vremenska postaja Tolmin' -annotate +10+80 'kamera S (fisheye)' -annotate +900+50 `date +%d.%m.%Y` -annotate +520+50 `date +%H:%M` $DIR/wcetemp.jpg $DIR/wcef.jpg

  fi

