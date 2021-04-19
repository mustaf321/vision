#include <Arduino.h>
#include <DHT.h>
#include <ESP8266WiFi.h>

#define DHTPIN 5
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

float t = 0.0;
float h = 0.0;

const char* ssid = "FRITZ!Box 7430 QS";
const char* password = "31649031723970168891";

WiFiServer server(80);

String header;


void setup() {
  // put your setup code here, to run once:
  dht.begin();
  Serial.println("Begin measure");
  Serial.begin(9600);

   Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    
    Serial.printf("Connection status: %d\n", WiFi.status());


  }
  // Lokale IP-Adresse im Seriellen Monitor ausgeben und Server starten
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  t = dht.readTemperature();
  h = dht.readHumidity();
  Serial.println("Temperature :" + String(t));
  Serial.println("Humidity :" + String(h));
  delay(5000);





 WiFiClient client = server.available();   // Auf Clients (Server-Aufrufe) warten

  if (client) {                             // Bei einem Aufruf des Servers
    Serial.println("Client available");
    String currentLine = "";                // String definieren für die Anfrage des Clients

    while (client.connected()) { // Loop, solange Client verbunden ist

      if (client.available()) {
        char c = client.read();             // Ein (1) Zeichen der Anfrage des Clients lesen
        Serial.write(c);                    // und es im Seriellen Monitor ausgeben
        header += c;
        if (c == '\n') {                    // bis eine Neue Zeile ausgegeben wird

          // Wenn der Client eine Leerzeile sendet, ist das Ende des HTTP Request erreicht
          if (currentLine.length() == 0) {

            // Der Server sendet nun eine Antwort an den Client
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            // Die Webseite anzeigen
            client.println("<!DOCTYPE html><html>");
            client.println("<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">");
            
            
            client.println("<link rel=\"icon\" href=\"data:,\"></head>");
            client.println("<body>");
            client.println("<h1 align=\"center\">Weather station</h1>");
            client.println("<h2 align=\"center\">Temperatur "+String(t)+" °C</h2>");
            client.println("<h2 align=\"center\">Luftfeuchte "+ String(h) +" %</h2>");
            client.println("</body></html>");

            // Die Antwort mit einer Leerzeile beenden
            client.println();
            // Den Loop beenden
            break;
          } else { // Bei einer Neuen Zeile, die Variable leeren
            currentLine = "";
          }
        } else if (c != '\r') {  // alles andere als eine Leerzeile wird
          currentLine += c;      // der Variable hinzugefüht
        }
      }
    }
    // Variable für den Header leeren
    header = "";
    // Die Verbindung beenden
    client.stop();
    Serial.println("Client disconnected");
    Serial.println("");
  }
}
