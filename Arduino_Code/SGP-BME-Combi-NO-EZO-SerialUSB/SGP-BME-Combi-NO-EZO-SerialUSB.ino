#include <SparkFunBME280.h>
#include "SparkFun_SGP40_Arduino_Library.h" 
#include <Wire.h>   

#define printtab(x) SerialUSB.print(String(x)+"\t");
#define printline SerialUSB.print("\n");

#define delaytime 1000

#define printtab(x) SerialUSB.print(String(x) + "\t");


SGP40 SGP; 
BME280 BME;

void setup() {                                        //set up the hardware
  SerialUSB.begin(9600);                                 //set baud rate for the hardware serial port_0 to 9600
  Wire.begin();
  if (SGP.begin() == false) {
    SerialUSB.println("No SGP40 Detected. Check connections.");
    while (!SGP.begin()){}
  }
  if (BME.begin() == false){
    SerialUSB.println("No BME280 Detected. Check connections.");
    while(!BME.begin()){}
  }
}


void loop() {                                         //here we go...
  SerialUSB.print(SGP.getVOCindex());
  SerialUSB.print(";");
  
  //printtab("Humidity: ");
  SerialUSB.print(BME.readFloatHumidity());
  SerialUSB.print(";");

  //printtab(" Pressure: ");
  SerialUSB.print(BME.readFloatPressure());
  SerialUSB.print(";");
  SerialUSB.print(BME.readTempC());
  SerialUSB.print(" ");

  delay(delaytime);                                       //act as if we have the third sensor installed - 3 sec loop
  SerialUSB.print("\n");
}
