#!/bin/sh

DIR=/home/pi/data
width=1600
height=1200

HOUR="$(date +'%H')"

  if [ $HOUR -ge 22 ] || [ $HOUR -lt 5 ] ; then
	raspistill -w $width -h $height -q 100 -o $DIR/wcetemp.jpg -ISO 800 -ss 2500000
#	convert -rotate 180 $DIR/wcetemp.jpg $DIR/wcetemp.jpg
	convert -pointsize 24 -fill white -annotate +10+50 'Vremenska postaja Solkan' -annotate +10+80 'www.i-tech.si/vreme' -annotate +1400+50 `date +%d.%m.%Y` -annotate +820+50 `date +%H:%M` $DIR/wcetemp.jpg $DIR/wcef.jpg
  else
	raspistill -w $width -h $height -q 100 -o $DIR/wcetemp.jpg
#	convert -rotate 180 $DIR/wcetemp.jpg $DIR/wcetemp.jpg
	convert -auto-level -pointsize 24 -fill black -annotate +10+50 'Vremenska postaja Solkan' -annotate +10+80 'www.i-tech.si/vreme' -annotate +1330+50 `date +%d.%m.%Y` -annotate +1460+50 'ob' -annotate +1500+50 `date +%H:%M` -annotate +1403+80 "kamera vzhod" $DIR/wcetemp.jpg $DIR/wce.jpg
        convert -composite $DIR/wce.jpg $DIR/itech_template.png $DIR/wcef.jpg

  fi
