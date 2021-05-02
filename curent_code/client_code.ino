#include <Arduino.h>
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <OneWire.h>
#include <ArduinoJson.h>
#include <ESP8266WiFiMulti.h>
#include <DallasTemperature.h>
#include <WiFiClientSecureBearSSL.h>

#define SERVER_IP ""
#define DHTPIN 5
#define DHTTYPE DHT11

const int oneWireBus = 4;
DHT dht(DHTPIN, DHTTYPE);
OneWire oneWire(oneWireBus);
DallasTemperature sensors(&oneWire);
float t = 0.0;
float h = 0.0;
char jsonOutput[128];
const char* ssid = "";
const char* password = "";
const size_t CAPACITY = JSON_OBJECT_SIZE(4);
StaticJsonDocument<CAPACITY> doc;





void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  dht.begin();
  sensors.begin();
  Serial.println("Begin measure");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected! IP address: ");
  Serial.println(WiFi.localIP());


}


void loop() {



  sensors.requestTemperatures();
  float temperatureC = sensors.getTempCByIndex(0);
  t = dht.readTemperature();
  h = dht.readHumidity();
  DynamicJsonDocument doc1(1024);
  JsonObject object = doc.to<JsonObject>();
  object["sensorID"] = "1";
  object["temperature"] = t ;
  object["humidity"] = h;
  object["SingleDS18B20"] = temperatureC;

  serializeJsonPretty(doc, jsonOutput);


  const char* m = object["sensorID"];
  delay(5000);
  if ((WiFi.status() == WL_CONNECTED)) {

    WiFiClient client;
    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    // configure traged server and url
    http.begin(client, "http://" SERVER_IP "/api/v1/temperatures/"+ String(m)); //HTTP
    http.addHeader("Content-Type", "application/json");

    Serial.print("[HTTP] PUT..." + String(jsonOutput) + "\n");
    // start connection and send HTTP header and body
    int httpCode = http.PUT(String(jsonOutput));

    // httpCode will be negative on error
    Serial.print(httpCode);
    if (httpCode > 0) {
      // HTTP header has been send and Server response header has been handled
      Serial.printf("[HTTP] PUT Response code: %d\n", httpCode);
      if (httpCode == 500) {http.end();
        http.begin(client, "http://" SERVER_IP "/api/v1/temperatures"); //HTTP
        http.addHeader("Content-Type", "application/json");

        Serial.print("[HTTP] post..." + String(jsonOutput) + "\n");
        // start connection and send HTTP header and body
        int httpCode = http.POST(String(jsonOutput));
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
