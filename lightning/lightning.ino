/***************************************************************************
* Designed for use with with Playing With Fusion AS3935 Lightning Sensor
* Breakout: SEN-39001-R01. Demo shows how this lightning sensor can be brought 
* into an Arduino project without a bunch of calibration needed. This is
* because each board is tested calibrated prior to being shipped, and the 
* cal value is written on the packaging.
*
*   SEN-39001-R01 (universal applications)
*   ---> http://www.playingwithfusion.com/productview.php?pdid=22
*
* Copyright © 2015 Playing With Fusion, Inc.
* SOFTWARE LICENSE AGREEMENT: This code is released under the MIT License.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
* **************************************************************************
* REVISION HISTORY:
* Author		Date		Comments
* J. Steinlage		2015Jul20       I2C release based on SPI example
* 
* Playing With Fusion, Inc. invests time and resources developing open-source
* code. Please support Playing With Fusion and continued open-source 
* development by buying products from Playing With Fusion!
*
* **************************************************************************
* APPLICATION SPECIFIC NOTES (READ THIS!!!):
* - This file configures then runs a program on an Arduino to interface with
*   an AS3935 Franklin Lightning Sensor manufactured by AMS.
*    - Configure Arduino
*    - Perform setup for AS3935 chip
*      --- capacitance registers for tuning (based on cal value provided)
*      --- configurations for your application specifics (indoor/outdoor, etc)
*    - read status/info from sensor
*    - Write formatted information to serial port
* - Set configs for your specific needs using the #defines for wiring, and
*   review the setup() function for other settings (indoor/outdoor, for example)
* - I2C specific note: This example uses the I2C interface via the I2C lib, not
*   the 'Wire' lib included with the Arduino IDE.
* 
* Circuit:
*    Arduino Uno   Arduino Mega  -->  SEN-39001: AS3935 Breakout
*    SDA:    SDA        SDA      -->  MOSI/SDA   (SDA is labeled on the bottom of the Arduino)
*    SCLK:   SCL        SCL      -->  SCK/SCL    (SCL is labeled on the bottom of the Arduino)
*    SI:     pin  9     pin 9    -->  SI (select interface; GND=SPI, VDD=I2C
*    IRQ:    pin  2     pin 2    -->  IRQ
*    GND:    GND        ''       -->  CS (pull CS to ground even though it's not used)
*    GND:    GND        ''       -->  GND
*    5V:     5V         ''       -->  Arduino I/O is at 5V, so power board from 5V. Can use 3.3V with Due, etc
**************************************************************************/

#include "I2C.h"
#include "PWFusion_AS3935_I2C.h"

volatile int8_t AS3935_ISR_Trig = 0;

#define SI_PIN               9
#define IRQ_PIN              2        // digital pins 2 and 3 are available for interrupt capability
#define AS3935_ADD           0x03     // x03 - standard PWF SEN-39001-R01 config
#define AS3935_CAPACITANCE   88       // <-- Value 88 pF

#define AS3935_INDOORS       1
#define AS3935_OUTDOORS      0
#define AS3935_DIST_DIS      0
#define AS3935_DIST_EN       1

void AS3935_ISR();

PWF_AS3935_I2C  lightning0((uint8_t)IRQ_PIN, (uint8_t)SI_PIN, (uint8_t)AS3935_ADD);

void setup()
{
   Serial.begin(115200);
 
  // setup for the the I2C library: (enable pullups, set speed to 400kHz)
  I2c.begin();
  I2c.pullup(true);
  I2c.setSpeed(1); 
  delay(2);
  
  lightning0.AS3935_DefInit();

  // now update sensor cal for your application and power up chip
  lightning0.AS3935_ManualCal(AS3935_CAPACITANCE, AS3935_OUTDOORS, AS3935_DIST_EN);
                                 // AS3935_ManualCal Parameters:
                                 //   --> capacitance, in pF (marked on package)
                                 //   --> indoors/outdoors (AS3935_INDOORS:0 / AS3935_OUTDOORS:1)
                                 //   --> disturbers (AS3935_DIST_EN:1 / AS3935_DIST_DIS:2)
                                 // function also powers up the chip
                  
  // enable interrupt (hook IRQ pin to Arduino Uno/Mega interrupt input: 0 -> pin 2, 1 -> pin 3 )
  attachInterrupt(0, AS3935_ISR, RISING);
  //lightning0.AS3935_PrintAllRegs();
  AS3935_ISR_Trig = 0;           // clear trigger

}

void loop()
{
  // This program only handles an AS3935 lightning sensor. It does nothing until 
  // an interrupt is detected on the IRQ pin.
  while(0 == AS3935_ISR_Trig){}
  delay(5);
  
  // reset interrupt flag
  AS3935_ISR_Trig = 0;
  
  // now get interrupt source
  uint8_t int_src = lightning0.AS3935_GetInterruptSrc();
  if(0 == int_src)
  {
  }
  else if(1 == int_src)
  {
    uint8_t lightning_dist_km = lightning0.AS3935_GetLightningDistKm();
    uint32_t lightning_energy = lightning0.AS3935_GetStrikeEnergyRaw();
    Serial.print(lightning_dist_km);
    Serial.print(",");
    Serial.println(lightning_energy);
  }
  else if(2 == int_src)
  {
  }
  else if(3 == int_src)
  {
  }

}

// this is irq handler for AS3935 interrupts, has to return void and take no arguments
// always make code in interrupt handlers fast and short
void AS3935_ISR()
{
  AS3935_ISR_Trig = 1;
}

