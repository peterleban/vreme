#!/usr/bin/env python
import urllib2,time
from datetime import datetime

# IP address of Wemos D1
url = "http://192.168.1.100"

# Sensor installation height
visina_senzorja = 123

# glavna zanka
while True:
	try:
		sneg = 0
		sneg_array = []
		for n in range(10):
			response = urllib2.urlopen(url, timeout=5)
			temp = int(response.read())
			sneg+= temp
			sneg_array.append(temp)
		sneg = max(sneg_array)
		debelina = visina_senzorja - sneg
		if debelina < 0:
			debelina = 0

# TODO: read temperature and use a compensated speed-of-sound value

# prebere trenutni cas (now) ter shrani v mesecno datoteko

	        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	        filename=datetime.now().strftime("/home/pi/sneg/data/%Y%m_sneg")
		file_sneg=open(filename,"a+")
		file_sneg.write("%s,%s\n" %(now,debelina))
		file_sneg.close()

# zapise samo trenutno vrednost v datoteko za prikaz na spletni strani
                file_sneg_last=open("sneg.txt","w")
                file_sneg_last.write("%s cm" %(debelina))
                file_sneg_last.close()

# ...vsakih 5 minut (300 sekund)
		time.sleep(300)
	except:
		pass

