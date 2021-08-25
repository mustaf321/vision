
#include <SPI.h>
#include <LoRa.h>
#include <Wire.h>
#include <DallasTemperature.h>
#include <DHT.h>
 

 
#define DHTPIN 5          //pin where the dht11 is connected
#define ss 15
#define rst 16
#define dio0 2
#define DHTTYPE DHT11
const int oneWireBus = 0;
OneWire oneWire(oneWireBus);
DHT dht(DHTPIN, DHT11);
DallasTemperature sensors(&oneWire);
float t = 0.0;
float h = 0.0; 
int counter = 0;
void setup() 
{
  Serial.begin(115200);
  dht.begin();
 

  
  while (!Serial);
  Serial.println("LoRa Sender");
  LoRa.setPins(ss, rst, dio0);
    if (!LoRa.begin(915E6)) {
    Serial.println("Starting LoRa failed!");
    delay(100);
    while (1);
  }
  

}
 
void loop() 
{



 sensors.requestTemperatures();
 float temperatureC = sensors.getTempCByIndex(0);
  t = dht.readTemperature();
  h = dht.readHumidity();
  delay(100);
 Serial.print("mesurment: "); 
 Serial.println(counter);
 Serial.print("temp: ");
 Serial.println(t);
 Serial.print("Hum :");
 Serial.println(h);
 Serial.print("temp2:");
 Serial.println(temperatureC);
 
 
  // send packet
  Serial.print("sending package: ");
  Serial.println(counter);  
  delay(3000);
  LoRa.beginPacket();
  LoRa.print(F("Pkt No:"));
  LoRa.println(counter);
  
  LoRa.print("Temp: ");
  LoRa.println(t);
  LoRa.print("Hum: ");
  LoRa.println(h);
  LoRa.print("Temp2: ");
  LoRa.println(temperatureC);
 
  
  LoRa.endPacket();
 
  counter++;
 
  delay(10000);
}
