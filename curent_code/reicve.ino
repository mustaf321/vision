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

#define SERVER_IP "172.28.128.1:8080"
String temp1;
String hum;
String del;

char jsonOutput[500];
const char* ssid = "WLAN-EUDSR4";
const char* password = "9704142346724801";
 
void setup() {
  Serial.begin(115200);
  
WiFi.begin(ssid, password);
int wifichek =0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    wifichek++;
    Serial.print(".");
  if(wifichek ==50)
  {Serial.println("");
    Serial.println("cannot connect with WIFI please check the ssid and Password and reset the Device");
    wifichek =0;
    }
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());




 
  Serial.println("LoRa Receiver Callback");
 
  LoRa.setPins(ss, rst);
 
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
 
  // register the receive callback
  LoRa.onReceive(onReceive);

 

  
}
 
void loop() {
  delay(3000);
   // put the radio into receive mode
  LoRa.receive();
 
   DynamicJsonDocument doc1(1024);
  JsonObject object = doc1.to<JsonObject>();
  object["nodeid"] = "1";
  object["temperature"] = temp1;
  object["humidity"] = hum;
  object["temperature2"] = del ;
  serializeJsonPretty(doc1, jsonOutput);
Serial.print(object);

   if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://127.0.0.1:8080/measurements/api/v1/temperatures/1"); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] PUT..." + String(jsonOutput) + "\n");
    // start connection and send HTTP header and body
 
   int httpCode = http.PUT(jsonOutput);
    
   // httpCode will be negative on error
    Serial.print(httpCode);
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] PUT Response code: %d\n", httpCode);
      if (httpCode == 500) {http.end();
        http.begin(client, "http://127.0.0.1:8080/measurements/api/v1/temperatures/1"); //HTTP
        http.addHeader("Content-Type", "application/json");

        Serial.print("[HTTP] post..." + String(jsonOutput)+ "\n");
        // start connection and send HTTP header and body
        
        Serial.printf("[HTTP] POST Response code: %d\n", httpCode);

      }


      // file found at server
      if (httpCode == HTTP_CODE_OK) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] POST... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();

    delay(10000);
  }
 }



void onReceive(int packetSize) {
  // received a packet
 
   char str[packetSize]=""; 
 
  // read packet
  for (int i = 0; i < packetSize; i++) {

  // revice bytes from lora
  byte b = LoRa.read();
 
  // translate bytes in to chars
  char demo = (char) b ;
  
  //save cahrs in arry
  str[i]=demo;
   
  }
  //create String out of the char arry
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


temp1 = String(String(res[19])+String(res[20])+String(res[21])+String(res[22])+String(res[23]));
hum = String(String(res[31])+String(res[32])+String(res[33])+String(res[34])+String(res[35]));
del = String(String(res[45])+String(res[46])+String(res[47])+String(res[48])+String(res[49]));

}
