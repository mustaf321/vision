#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <DallasTemperature.h>
#include <DHT.h>
 

 
#define DHTPIN 5          //pin where the dht11 is connected
#define ss 15
#define rst 2
#define nodeid "1" 
#define dio0 5
#define DHTTYPE DHT11
byte localAddress = 0x02;     // address of this device
byte destination = 0x01;      // destination to send to
String outgoing;  
const int oneWireBus = 0;
OneWire oneWire(oneWireBus);
DHT dht(DHTPIN, DHT11);
DallasTemperature sensors(&oneWire);
float t = 0.0;
float h = 0.0; 
float temperatureC =0.0; 
int counter = 0;
int Loralook = 0;
void setup() 
{
  Serial.begin(115200);
  dht.begin();
  
  // Deep sleep mode for 30 seconds, the ESP8266 wakes up by itself when GPIO 16 (D0 in NodeMCU board) is connected to the RESET pin

  

  
  while (!Serial);
  Serial.println("LoRa Sender");
  LoRa.setPins(ss, rst,dio0
  );
    if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
   
    while (1);
  }
  
  
}


void loop() 
{


//Serial.print(Loralook);
 
Serial.println("good moring");  
 int order=onReceive(LoRa.parsePacket());
 
  if(order==1){
    
    gatherInfo();
    
    }// send packet  Serial.println("I'm awake, but I'm going into deep sleep mode for 30 seconds");
      

 
}

void sendMessage(String outgoing) {
  LoRa.beginPacket();                   // start packet

  LoRa.write(destination);              // add destination address
  LoRa.write(localAddress);             // add sender address
  LoRa.write(counter);                 // add message ID
  LoRa.write(outgoing.length());        // add payload length
  LoRa.print(outgoing);                 // add payload
  LoRa.endPacket();                     // finish packet and send it
  counter++;                           // increment message ID
}

int onReceive(int packetSize) {
  Serial.println(packetSize);
  if (packetSize == 0) return 0;          // if there's no packet, return

  // read packet header bytes:
  int recipient = LoRa.read();          // recipient address
  byte sender = LoRa.read();            // sender address
  byte incomingMsgId = LoRa.read();     // incoming msg ID
  byte incomingLength = LoRa.read();    // incoming msg length
 
 
  String incoming = "";

  while (LoRa.available()) {
    incoming += (char)LoRa.read();
  }
  Serial.print("incommin.length ist ");
  Serial.println( incoming.length());
  
  Serial.print("incomingLength ist ");
  Serial.println( incomingLength);
  if (incomingLength != incoming.length()) {   // check length for error
    Serial.println("error: message length does not match length");
    
    delay(100);
    
       return 0 ;                             // skip rest of function
  }

  // if the recipient isn't this device or broadcast,
  if (recipient != localAddress && recipient != 0xFF) {
    Serial.println("This message is not for me.");
    return 0;                             // skip rest of function
  }
 
  // if message is for this device, or broadcast, print details:
  Serial.println("Received from: 0x" + String(sender, HEX));
  Serial.println("Sent to: 0x" + String(recipient, HEX));
  Serial.println("Message ID: " + String(incomingMsgId));
  Serial.println("Message length: " + String(incomingLength));
  Serial.println("Message: " + incoming);
  Serial.println("RSSI: " + String(LoRa.packetRssi()));
  Serial.println("Snr: " + String(LoRa.packetSnr()));
  Serial.println();
  if(incoming=="s")
  {
    return 1;
    } 
   else{
    return 0 ;
    
    }
}

void gatherInfo(){
    sensors.requestTemperatures();
    float temperatureC = sensors.getTempCByIndex(0);
    t = dht.readTemperature();
    h = dht.readHumidity();
    delay(100);
    Serial.print("mesurment: "); 
    Serial.println(counter);
    Serial.print("nodeid:");
    Serial.println(nodeid);
    Serial.print("temp: ");
    Serial.println(t);
    Serial.print("Hum :");
    Serial.println(h);
    Serial.print("temp2:");
    Serial.println(temperatureC);
    String data = String(nodeid+String(t)+String(h)+String(temperatureC));
    Serial.print("sending package: ");
    Serial.println(data);
    delay(500);
    sendMessage(data);
   
    Serial.print("sending package: ");
    Serial.println(counter);  
    Serial.println("good nigth");
    ESP.deepSleep(10e6); 
  }
