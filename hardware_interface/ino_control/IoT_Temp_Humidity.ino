#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"

// -----------  WiFi & MQTT Configuration
const char* ssid = "WIFI ID HERE";
const char* password = "PASSWORD HERE";
const char* mqtt_server = "MQTT BROKER IP HERE";

WiFiClient espClient;
PubSubClient client(espClient);

// ----------- DHT Configuration
#define DHTPIN 21
#define DHTTYPE DHT11
#define dht(DHTPIN, DHTTYPE);

// ----------- MQTT Callback
void callback(char* topic, byte* payload, unsigned int length) 
{
  Serial.print("[Server > ESP32] -- ");
  Serial.print(topic);
  
  for (int i = 0; i < length; i++) 
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
  // INSERT COMMAND HANDLING HERE.
}

// ----------- MQTT Reconnect
void reconnect() 
{
  while (!client.connected()) 
  {
    Serial.print("Attempting MQTT connection...");
    
    if (client.connect("ESP32-DHT")) 
    {
      Serial.println("Connected.");
      client.subscribe("commands/room"); // example subscription
    } 
    else 
    {
      Serial.print("Failed, rc = ");
      Serial.print(client.state());
      delay(5000);
    }
  }
}

// ----------- Setup
void setup()
{
  Serial.begin(115200);
  dht.begin();

  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected.")

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// ----------- Loop
void loop() 
{
  if (!client.connected()) 
  {
    reconnect();
  }
  client.loop();

  static unsigned long last_message = 0;
  unsigned long now = millis();
  
  if (now - last_message > 3000) // Publishes every 3 seconds.
  {
    last_message = now;
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (isnan(humidity) || isnan(temperature)) 
    {
      Serial.println("Failed to read from DHT sensor!");
      return;
    }

    // Format JSON payload
    char payload[100];
    snprintf(payload, sizeof(payload), "{ \"temperature\": %.2f, \"humidity\": %.2f }", temperature, humidity);

    client.publish("sensors/room_condition", payload);
    Serial.println(payload);
  }
}
