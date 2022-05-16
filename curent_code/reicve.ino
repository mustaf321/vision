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
#define SERVER_IP "192.168.2.120:8080"
String temp1;
String hum;
String del;
String nodeid;
String res ="";
char jsonOutput[500];
const char* ssid = "WLAN-EUDSR4";
const char* password = "9704142346724801";
const size_t CAPACITY = JSON_OBJECT_SIZE(6);
StaticJsonDocument<CAPACITY> doc; 


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


nodeid = String(String(res[0]));
temp1 = String(String(res[1])+String(res[2])+String(res[3])+String(res[4])+String(res[5]));
 
hum = String(String(res[6])+String(res[7])+String(res[8])+String(res[9])+String(res[10]));
del = String(String(res[11])+String(res[12])+String(res[13])+String(res[14])+String(res[15]));




}
void setup() {
  Serial.begin(115200);
  while (!Serial);

WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());




 
  Serial.println("LoRa Receiver Callback");
 
  LoRa.setPins(ss, rst, dio0);
 
  if (!LoRa.begin(868E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
 
  // register the receive callback
  LoRa.onReceive(onReceive);

 delay(500);

  
}
 
void loop() {
  delay(3000);
   // put the radio into receive mode
  LoRa.receive();
 
   DynamicJsonDocument doc1(1024);
  JsonObject object = doc.to<JsonObject>();
  object["nodeid"] = nodeid;
  object["temperature"] = temp1;
  object["humidity"] = hum;
  object["temperature2"] = del ;
  serializeJsonPretty(doc, jsonOutput);


   if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://"SERVER_IP"/measurements/api/v1/temperatures/1"); //HTTP
    http.addHeader("Content-Type", "application/json");
    
    Serial.print("[HTTP] PUT..." + String(jsonOutput) + "\n");
    // start connection and send HTTP header and body

   int httpCode = http.PUT(jsonOutput);
    
    Serial.print("ICh bin hier!!!!!!!");
    // httpCode will be negative on error
    Serial.print(httpCode);
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] PUT Response code: %d\n", httpCode);
      if (httpCode == 500) {http.end();
        http.begin(client, "http://" SERVER_IP "/measurements/api/v1/temperatures/1"); //HTTP
        http.addHeader("Content-Type", "application/json");

   
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
