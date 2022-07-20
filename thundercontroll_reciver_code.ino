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
#define SERVER_IP "000.0000.0.2:8080"
String temp1;
String hum;
String del;
String nodeid;
String outgoing;  
char jsonOutput[500];
int httplook = 0;
int restcnt = 0;
const char* ssid = "MagentaWLAN-GOO0";
const char* password = "66624299097758068976";
const size_t CAPACITY = JSON_OBJECT_SIZE(6);
StaticJsonDocument<CAPACITY> doc; 
byte localAddress = 0x01;     // address of this device
byte destination = 0x02;      // destination to send to
int lastSendTime=0;
int interval=0;
int msgCount=0;
void setup() {
  Serial.begin(115200);
  
WiFi.begin(ssid, password);
int wifichek =0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    wifichek++;
    Serial.print(".");
  if(wifichek ==100)
  {Serial.println("");
    Serial.println("cannot connect with WIFI please check the ssid and Password and reset the Device");
    wifichek =0;
    }
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());




 
  Serial.println("LoRa Receiver Callback");
 
  LoRa.setPins(ss, rst, dio0);
 
  if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    while (1);
  }
 

  LoRa.onReceive(onReceive);
  LoRa.receive();
  Serial.println("LoRa init succeeded.");
  
  
}
 
void loop() {
  // register the receive callback
  if (millis() - lastSendTime > interval) {
    String message = "s";   // send a message
    sendMessage(message);
    Serial.println("Sending " + message);
    lastSendTime = millis();            // timestamp the message
    interval = random(2000) + 1000;    // 2-3 seconds
   

 if(httplook==1){
   DynamicJsonDocument doc1(1024);
  JsonObject object = doc.to<JsonObject>();
  object["nodeid"] = nodeid ;
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
    

    // httpCode will be negative on error
    Serial.print(httpCode);
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] PUT Response code: %d\n", httpCode);
      if (httpCode == 500) {
        Serial.printf("[HTTP] PUT... failed, error: %s\n", http.errorToString(httpCode).c_str());
     
      }


      // file found at server
      if (httpCode == 200) {
        const String& payload = http.getString();
        Serial.println("received payload:\n<<");
        Serial.println(payload);
        Serial.println(">>");
      }
    } else {
      Serial.printf("[HTTP] PUT... failed, error: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
    httplook=0;
    delay(10000);
  }
 } 
LoRa.receive();
  
 }
}

void sendMessage(String outgoing) {
  LoRa.beginPacket();                   // start packet
  LoRa.write(destination);              // add destination address
  LoRa.write(localAddress);             // add sender address
  LoRa.write(msgCount);                 // add message ID
  LoRa.write(outgoing.length());        // add payload length
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  msgCount++;                           // increment message ID
}


void onReceive(int packetSize) {

  Serial.println("recviermode!!");
  if (packetSize == 0) return;          // if there's no packet, return
  
  // read packet header bytes:
  int recipient = LoRa.read();          // recipient address
  byte sender = LoRa.read();            // sender address
  byte incomingMsgId = LoRa.read();     // incoming msg ID
  byte incomingLength = LoRa.read();    // incoming msg length

  String incoming = "";                 // payload of packet
  char str[packetSize];
  while (LoRa.available()) {            // can't use readString() in callback, so
    incoming += (char)LoRa.read();      // add bytes one by one
  }
    httplook=1;
 // if (incomingLength != incoming.length()) {   // check length for error
   // Serial.println("error: message length does not match length");
   // return;                             // skip rest of function
 // }

  // if the recipient isn't this device or broadcast,
  if (recipient != localAddress && recipient != 0xFF) {
    Serial.println("This message is not for me.");
    return;                             // skip rest of function
  }

  // if message is for this device, or broadcast, print details:
  Serial.println("Received from: 0x" + String(sender, HEX));
  Serial.println("Sent to: 0x" + String(recipient, HEX));
  Serial.println("Message ID: " + String(incomingMsgId));
  Serial.println("Message length: " + String(incomingLength));

  Serial.println("temp1 is: " + incoming.substring(1,6));
  temp1=incoming.substring(1,6);
  Serial.println("hium is: " + incoming.substring(7,11));
  hum=incoming.substring(6,11);
  Serial.println("temp2 is: " + incoming.substring(8,16));
  del=incoming.substring(11,16);
  nodeid =  String(sender);
  
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + String(LoRa.packetRssi()));
  Serial.println("Snr: " + String(LoRa.packetSnr()));
  Serial.println();
}
