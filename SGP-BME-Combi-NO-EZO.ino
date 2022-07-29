
#include <SoftwareSerial.h>                           
#include <SparkFunBME280.h>
#include "SparkFun_SGP30_Arduino_Library.h" 
#include <Wire.h>

#define printtab(x) Serial.print(String(x)+"\t");
#define printline Serial.print("\n");

//#define rx1 2                                          //define what pin rx is going to be
//#define tx1 3                                          //define what pin tx is going to be
//#define rx2 4
//#define tx2 5
#define delaytime 1000

#define printtab(x) Serial.print(String(x) + "\t");

//SoftwareSerial CO2port (rx1, tx1);                      //define how the soft serial port is going to work
//SoftwareSerial O2port (rx2, tx2);
SGP30 SGP; 
BME280 BME;

String inputstring = "";                              //a string to hold incoming data from the PC
String CO2_sensorstring = "";                             //a string to hold the data from the Atlas Scientific product
String O2_sensorstring = "";
boolean input_string_complete = false;                //have we received all the data from the PC
boolean CO2_sensor_string_complete = false;               //have we received all the data from the Atlas Scientific product
boolean O2_sensor_string_complete = false;
int Co2;                                              //used to hold a integer number that is the Co2
int o2;



void setup() {                                        //set up the hardware
  Serial.begin(9600);                                 //set baud rate for the hardware serial port_0 to 9600
//  CO2port.begin(9600);                               //set baud rate for the software serial port to 9600
//  O2port.begin(9600);
  Wire.begin();
  if (SGP.begin() == false) {
    Serial.println("No SGP30 Detected. Check connections.");
    while (!SGP.begin()){}
  }
  if (BME.begin() == false){
    Serial.println("No BME280 Detected. Check connections.");
    while(!BME.begin()){}
  }
  SGP.initAirQuality();
  inputstring.reserve(10);                            //set aside some bytes for receiving data from the PC
  while(!Serial){}

//  CO2_sensorstring.reserve(30);                           //set aside some bytes for receiving data from Atlas Scientific product
//  O2_sensorstring.reserve(30);
}


void serialEvent() {                                  //if the hardware serial port_0 receives a char
  inputstring = Serial.readStringUntil(13);           //read the string until we see a <CR>
  input_string_complete = true;                       //set the flag used to tell if we have received a completed string from the PC
}


void loop() {                                         //here we go...

//  if (input_string_complete == true) {                //if a string from the PC has been received in its entirety
//    CO2port.print(inputstring);                      //send that string to the Atlas Scientific product
//    CO2port.print('\r');                             //add a <CR> to the end of the string
//
//    Serial.println();
//    Serial.println("input_string_complete == true");
//    Serial.println();
//    
//    delay(10);
//    O2port.print(inputstring);
//    O2port.print('\r');
//    inputstring = "";                                 //clear the string
//    input_string_complete = false;                    //reset the flag used to tell if we have received a completed string from the PC
//    delay(10);
//  }
//  
//  CO2port.listen();
//  delay(delaytime);
//  while (CO2port.available() > 0) {                     //if we see that the Atlas Scientific product has sent a character
//    char inchar = (char)CO2port.read();              //get the char we just received
//    CO2_sensorstring += inchar;                           //add the char to the var called sensorstring
//    if (inchar == '\r') {                             //if the incoming character is a <CR>
//      CO2_sensor_string_complete = true;                  //set the flag
//    }
//  }
//
//  O2port.listen();
//  delay(delaytime);
//  while (O2port.available() > 0) {
//    char inchar = (char)O2port.read();
//    O2_sensorstring += inchar;
//    if (inchar == '\r') {                             //if the incoming character is a <CR>
//      O2_sensor_string_complete = true;                  //set the flag
//    }
//  }
//  for(int i = 0; i<sizeof(CO2_sensorstring)-1;i++){
//   if(CO2_sensorstring[i] == 0x0a){
//      CO2_sensorstring[i] = '\0';
//   }
//   else if(CO2_sensorstring[i] == '\r'){
//      CO2_sensorstring[i] = '\0';
//   }
//  }
//  for(int i = 0; i<sizeof(O2_sensorstring)-1;i++){
//   if(O2_sensorstring[i] == 0x0a){
//      O2_sensorstring[i] = '\0';
//   }
//   else if(O2_sensorstring[i] == '\r'){
//      O2_sensorstring[i] = '\0';
//   }
//  }
  SGP.measureAirQuality();
  Serial.print(SGP.CO2);
  Serial.print(";");
  Serial.print(SGP.TVOC);
  Serial.print(";");
  
  //printtab("Humidity: ");
  Serial.print(BME.readFloatHumidity());
  Serial.print(";");

  //printtab(" Pressure: ");
  Serial.print(BME.readFloatPressure());
  Serial.print(";");
  Serial.print(BME.readTempC());
  Serial.print(" ");
//  Serial.print(":");



//  if (O2_sensor_string_complete == true && CO2_sensor_string_complete == true) {               //if a string from the Atlas Scientific product has been received in its entirety
//    
//    char CO2String[32];
//    int newsize=0;
//    for(int i = 0; i<sizeof(CO2_sensorstring)-1;i++)
//    {
//       if(CO2_sensorstring[i] != '\n' && CO2_sensorstring[i] != '\r')
//          CO2String[newsize++]=CO2_sensorstring[i];   
//    }
//
//    char O2String[32];
//    newsize=0;
//    for(int i = 0; i<sizeof(O2_sensorstring)-1;i++)
//    {
//       if(O2_sensorstring[i] != '\n' && O2_sensorstring[i] != '\r')
//          O2String[newsize++]=O2_sensorstring[i];   
//    }
//
//    Serial.print(O2_sensorstring + ";");
//    Serial.print(CO2_sensorstring + ";");                     //send that string to the PC's serial monitor
//
//    CO2_sensorstring = "";                                //clear the string
//    O2_sensorstring = "";
//    CO2_sensor_string_complete = false;
//    O2_sensor_string_complete = false;
//  }
//
//  else if (O2_sensor_string_complete == true &&  CO2_sensor_string_complete == false){
//    printtab("CO2_nodata");
//    printtab(O2_sensorstring + "\n");
//
//    CO2_sensorstring = "";                                //clear the string
//    O2_sensorstring = "";
//    CO2_sensor_string_complete = false;
//    O2_sensor_string_complete = false;
//  }
//  else if (O2_sensor_string_complete == false && CO2_sensor_string_complete == true){
//    printtab(CO2_sensorstring);
//    printtab("O2_nodata\n");
//
//    CO2_sensorstring = "";
//    O2_sensorstring = "";
//    CO2_sensor_string_complete = false;
//    O2_sensor_string_complete = false;
//  }
//
//  else{
//    printtab("CO2_nodata");
//    printtab("O2_nodata\n");
//
//    CO2_sensorstring = "";                                //clear the string
//    O2_sensorstring = "";
//    CO2_sensor_string_complete = false;                   //reset the flag used to tell if we have received a completed string from the Atlas Scientific product
//    O2_sensor_string_complete = false;
//  }
  delay(delaytime);                                       //act as if we have the third sensor installed - 3 sec loop
  Serial.print("\n");
}
