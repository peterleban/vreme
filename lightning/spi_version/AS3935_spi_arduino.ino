/*
  LightningDetector.pde - AS3935 Franklin Lightning Sensor™ IC by AMS library demo code
  Copyright (c) 2012 Raivis Rengelis (raivis [at] rrkb.lv). All rights reserved.

  This library is free software; you can redistribute it and/or
  modify it under the terms of the GNU Lesser General Public
  License as published by the Free Software Foundation; either
  version 3 of the License, or (at your option) any later version.

  This library is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  Lesser General Public License for more details.

  You should have received a copy of the GNU Lesser General Public
  License along with this library; if not, write to the Free Software
  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/

#include <SPI.h>
#include <AS3935.h>

void printAS3935Registers();

// Function prototype that provides SPI transfer and is passed to
// AS3935 to be used from within library, it is defined later in main sketch.
// That is up to user to deal with specific implementation of SPI
// Note that AS3935 library requires this function to have exactly this signature
// and it can not be member function of any C++ class, which happens
// to be almost any Arduino library
// Please make sure your implementation of choice does not deal with CS pin,
// library takes care about it on it's own
byte SPItransfer(byte sendByte);

// Iterrupt handler for AS3935 irqs
// and flag variable that indicates interrupt has been triggered
// Variables that get changed in interrupt routines need to be declared volatile
// otherwise compiler can optimize them away, assuming they never get changed
void AS3935Irq();
volatile int AS3935IrqTriggered;

// First parameter - SPI transfer function, second - Arduino pin used for CS
// and finally third argument - Arduino pin used for IRQ
// It is good idea to chose pin that has interrupts attached, that way one can use
// attachInterrupt in sketch to detect interrupt
// Library internally polls this pin when doing calibration, so being an interrupt pin
// is not a requirement

// Edit: July 16, 2020
// This code was modified to work on Arduino Nano
// with Lightning detector from playingwithfusion.com
// End edit

#define IRQpin 2
#define CSpin 10

AS3935 AS3935(SPItransfer,CSpin,IRQpin);

void setup()
{
  Serial.begin(115200);
  // first begin, then set parameters
  SPI.begin();
  // NB! chip uses SPI MODE1
  SPI.setDataMode(SPI_MODE1);
  // NB! max SPI clock speed that chip supports is 2MHz,
  // but never use 500kHz, because that will cause interference
  // to lightning detection circuit
  SPI.setClockDivider(SPI_CLOCK_DIV16);
  // and chip is MSB first
  SPI.setBitOrder(MSBFIRST);
  // reset all internal register values to defaults
  AS3935.reset();
  // and run calibration
  // if lightning detector can not tune tank circuit to required tolerance,
  // calibration function will return false
  
  //if(!AS3935.calibrate())
  //  Serial.println("Tuning out of range, check your wiring, your sensor and make sure physics laws have not changed!");

  outputCalibrationValues();
  recalibrate();

  // Setting the watchdog threshold to higher value prevents false positives but reduces sensitivity to real strikes
  // Setting the spike rejection to higher value prevents false positives but reduces sensitivity to real strikes
  AS3935.setNoiseFloor(1);
  AS3935.setSpikeRejection(2);
  AS3935.setWatchdogThreshold(3);
  
  outputCalibrationValues();
  recalibrate();

  // first let's turn on disturber indication and print some register values from AS3935
  // tell AS3935 we are indoors, for outdoors use setOutdoors() function
  AS3935.setIndoors();
  //AS3935.setOudoors();

  // turn on indication of distrubers, once you have AS3935 all tuned, you can turn those off with disableDisturbers()
  AS3935.enableDisturbers();
  //AS3935.disableDisturbers();

  printAS3935Registers();
  AS3935IrqTriggered = 0;

  attachInterrupt(0,AS3935Irq,RISING);
}

void loop()
{
  if(AS3935IrqTriggered)
  {
    AS3935IrqTriggered = 0;
    // wait 2 ms before reading register (according to datasheet?)
    delay(2);
    // first step is to find out what caused interrupt
    // as soon as we read interrupt cause register, irq pin goes low
    int irqSource = AS3935.interruptSource();
    // returned value is bitmap field, bit 0 - noise level too high, bit 2 - disturber detected, and finally bit 3 - lightning!
    if (irqSource & 0b0001)
      Serial.println("NOISE");
    if (irqSource & 0b0100)
      Serial.println("DISTURBER");
    if (irqSource & 0b1000)
    {
      int strokeDistance = AS3935.lightningDistanceKm();
      int strokeEnergy = AS3935.lightningEnergy();
        Serial.print("S");
        Serial.print(strokeDistance,DEC);
        Serial.print(",");
        Serial.println(strokeEnergy,DEC);

    }
  }
}

void printAS3935Registers()
{
  int noiseFloor = AS3935.getNoiseFloor();
  int spikeRejection = AS3935.getSpikeRejection();
  int watchdogThreshold = AS3935.getWatchdogThreshold();
  int minLightning = AS3935.getMinimumLightnings();
  Serial.print("C Noise floor is: ");
  Serial.println(noiseFloor,DEC);
  Serial.print("C Spike rejection is: ");
  Serial.println(spikeRejection,DEC);
  Serial.print("C Watchdog threshold is: ");
  Serial.println(watchdogThreshold,DEC); 
  Serial.print("C Minimum Lightning is: ");
  Serial.println(minLightning,DEC);   
}

byte SPItransfer(byte sendByte)
{
  return SPI.transfer(sendByte);
}

void AS3935Irq()
{
  AS3935IrqTriggered = 1;
}


void recalibrate() {
  delay(50);
  Serial.println();
  int calCap = AS3935.getBestTune();
  Serial.print("C antenna calibration picks value:\t ");
  Serial.println(calCap);
  delay(50);
}

void outputCalibrationValues() {
   // output the frequencies that the different capacitor values set:
  delay(50);
  Serial.println();
  for (byte i = 0; i <= 0x0F; i++) {
    int frequency = AS3935.tuneAntenna(i);
    Serial.print("C tune antenna to capacitor ");
    Serial.print(i);
    Serial.print("\t gives frequency: ");
    Serial.print(frequency);
    Serial.print(" = ");
    long fullFreq = (long) frequency*160;  // multiply with clock-divider, and 10 (because measurement is for 100ms)
    Serial.print(fullFreq,DEC);
    Serial.println(" Hz");
    delay(10);
  }
}
