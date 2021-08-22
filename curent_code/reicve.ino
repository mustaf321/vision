#include <SPI.h>
#include <LoRa.h>
#include <Arduino.h>
#include <WiFiClientSecureBearSSL.h>
#include <ESP8266WiFiMulti.h>
#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
 
#define ss 15
#define rst 16
#define dio0 4


float t = 0.0;
float h = 0.0;
char jsonOutput[500];
const char* ssid = "";
const char* password = "";
const size_t CAPACITY = JSON_OBJECT_SIZE(6);
StaticJsonDocument<CAPACITY> doc; 
void setup() {
  Serial.begin(115200);
  while (!Serial);
 
  Serial.println("LoRa Receiver Callback");
 
  LoRa.setPins(ss, rst, dio0);
 
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
 
  // register the receive callback
  LoRa.onReceive(onReceive);
 
  // put the radio into receive mode
  
}
 
void loop() {
  delay(3000);
  LoRa.receive();
  // do nothing
}



 
void onReceive(int packetSize) {
  // received a packet
 
   char str[packetSize]=""; 
 
  // read packet
  for (int i = 0; i < packetSize; i++) {

  byte b = LoRa.read();
 

  char demo = (char) b ;
  
  str[i]=demo;
   

 
  }

  String res ="";
 
   for(int j=0;j< packetSize; j++ ){
   

   res=res+String (str[j]);

  
   }

Serial.println("revied package:");  
Serial.println("---------");
Serial.print("Package size:");
Serial.println(packetSize);
Serial.println(res);
 
// print RSSI of packet
Serial.print("with RSSI ");
Serial.println(LoRa.packetRssi());
Serial.println("---------");


String temp1 = String(String(res[19])+String(res[20])+String(res[21])+String(res[22])+String(res[23]));
Serial.println(temp1);
String hum = String(String(res[31])+String(res[32])+String(res[33])+String(res[34])+String(res[35]));
Serial.println(hum);
String del = String(String(res[45])+String(res[46])+String(res[47])+String(res[48])+String(res[49]));
Serial.println(del);

DynamicJsonDocument doc1(1024);
  JsonObject object = doc.to<JsonObject>();
  object["sensorID"] = "1";
  object["Temp:"] = temp1;
  object["Hum:"] = hum;
  object["Temp2:"] = del ;
  serializeJsonPretty(doc, jsonOutput);
Serial.print(jsonOutput);  
 
}
