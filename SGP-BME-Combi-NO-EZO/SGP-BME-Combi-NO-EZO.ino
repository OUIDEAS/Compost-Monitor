#include <SparkFun_SGP40_Arduino_Library.h>
#include <sensirion_arch_config.h>
#include <sensirion_voc_algorithm.h>
#include <SparkFunBME280.h> 
#include <Wire.h>   

#define printtab(x) Serial.print(String(x)+"\t");
#define printline Serial.print("\n");
#define delaytime 1000
#define printtab(x) Serial.print(String(x) + "\t");


SGP40 SGP; 
BME280 BME;

void setup() {                                        //set up the hardware
  Serial.begin(9600);                                 //set baud rate for the hardware serial port_0 to 9600
  Wire.begin();
  if (SGP.begin() == false) {
    Serial.println("No SGP40 Detected. Check connections.");
    while (!SGP.begin()){}
  }
  if (BME.begin() == false){
    Serial.println("No BME280 Detected. Check connections.");
    while(!BME.begin()){}
  }
}


void loop() {                                         //here we go...
  Serial.print(SGP.getVOCindex());
  Serial.print(";");
  
  //printtab("Humidity: ");
  Serial.print(BME.readFloatHumidity());
  Serial.print(";");

  //printtab(" Pressure: ");
  Serial.print(BME.readFloatPressure());
  Serial.print(";");
  Serial.print(BME.readTempC());
  Serial.print(" ");

  delay(delaytime);                                       //act as if we have the third sensor installed - 3 sec loop
  Serial.print("\n");
}
