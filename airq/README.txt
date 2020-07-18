Skripti za branje podatkov s senzorjev:

    LUFFTDATEN SDS011
    HONEYWELL HPMA115S0


***************************    LUFFTDATEN SDS011    **************************
    readAQI.py

Senzor Lufftdaten SDS011 / Nova sensor

Prebere vrednosti PM2.5 in PM10 ter ju shrani v datoteki:
   aqi.json ... trenutne vrednosti, datoteka je kompatibilna z Weather Display
   AQI_YYYY_mm.log ... vrednosti v zadnjem mesecu

Ob zagonu se vklopi ventilator, ki požene zrak mimo fotodiode.
Prvih 10 izmerkov pri preračunu ne upošteva. Nadaljnjih 5 izmerkov povpreči
in zapiše v datoteki.

Format Weather Display datoteke:
    <PM10>,<PM2.5>

Format mesečne datoteke:
    <epoch>,<PM2.5>,<PM10>


Fotosenzor ima omejeno življenjsko dobo, zato je zagon skripta priporočljivo
nastaviti na vsakih par minut (npr. 3-5 minut).
Primer nastavitve v 'crontab':

    */5 * * * * /usr/bin/python /home/pi/scripts/readAQI.py




***************************    HONEYWELL HPMA115S0  **************************

    readHoneywell.py

Senzor Honeywell HPMA115S0

Ob zagonu se v senzorju požene ventilator, ki požene zrak mimo fotosenzorja.
Po 10 sekundah se izvede serija 10 meritev, rezultat je povprečje.
Podatki se zapišejo v datoteko 'airq.txt', ki jo nato prebere 'weewx' in vrednosti
shrani v svojo SQL bazo.

Honeywellov senzor načeloma nima omejene življenjsko dobo (oz cca 10 let),
vseeno je zagon skripta priporočljivo nastaviti na vsakih par minut (npr. 3-5 minut).
Primer nastavitve v 'crontab':

    */5 * * * * /usr/bin/python /home/pi/scripts/readHoneywell.py
