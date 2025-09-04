#include <WiFi.h>
#include <PubSubClient.h>

// ----------- WiFi & MQTT Configuration
const char* ssid = "WIFI ID HERE";
const char* password = "PASSWORD HERE";
const char* mqtt_server = "MQTT BROKER IP HERE";

WiFiClient espClient; 
PubSubClient client(espClient);

// ----------- Pin Mapping
#define US_T1_01_TRIG 16
#define US_T1_01_ECHO 17
#define US_T1_02_TRIG 18
#define US_T1_02_ECHO 19
#define US_T2_01_TRIG 21
#define US_T2_01_ECHO 22
#define US_T2_02_TRIG 4
#define US_T2_02_ECHO 5

// ----------- Internal Functions

long readUltrasonic(int trig_pin, int echo_pin)
{
  digitalWrite(trig_pin, LOW);
  delayMicroseconds(2);
  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);

  long duration = pulseIn(echo_pin, HIGH, 30000);
  long distance = duration * 0.0343 / 2;

  return distance == 0 ? -1 : distance;
}

// ----------- MQTT Callback
void callback(char* topic, byte* payload, unsigned int length)
{
  Serial.print("[Server > ESP32] -- ");
  Serial.print(topic);

  for (int i = 0; i < length; i++)
  {
    Serial.print((char) paylaod[i]);
  }
  Serial.println();
  
  // NOTE TO SELF: PLEASE INCLUDE ALL REACTIONS TO CONTROL COMMANDS HERE...
  
}

// ----------- MQTT Reconnect
void reconnect()
{
  while (!client.connected())
  {
    Serial.pritn("Attempting MQTT connection...");
    if(client.connect("ESP32-SeatHogger"))
    {
      Serial.pritnln("Connected.");
      client.subscribe("comamnds/room"); // CHANGE TO SPECIFIC SUBSCRIPTION LINK
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

  pinMode(US_T1_01_TRIG, OUTPUT); pinMode(US_T1_01_ECHO, INPUT);
  pinMode(US_T1_02_TRIG, OUTPUT); pinMode(US_T1_02_ECHO, INPUT);
  pinMode(US_T2_01_TRIG, OUTPUT); pinMode(US_T2_01_ECHO, INPUT);
  pinMode(US_T2_02_TRIG, OUTPUT); pinMode(US_T2_02_ECHO, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500)
    Serial.print(".");
  }
  Serial.println("\nWiFi Connection Successful.")

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

// ----------- Loop
void loop()
{
  if (!client.conected())
  {
    reconnect();
  }
  client.loop();

  static unsigned long last_message = 0; 
  unsigned long now = millis();
  if (now - last_message > 3000) // Publishes data every 3 seconds HERE.
  {
    last_message = now;
  
    long d_t1_top = readUltrasonic(US_T1_01_TRIG, US_T1_01_ECHO)
    long d_t1_bottom = readUltrasonic(US_T1_02_TRIG, US_T1_02_ECHO);
    long d_t2_top = readUltrasonic(US_T2_01_TRIG, US_T2_01_ECHO);
    long d_t2_bottom = readUltrasonic(US_T2_02_TRIG, US_T2_02_ECHO);

    char payload[200];
    snprintf(payload, sizeof(payload), "{ \"T1_top\": %ld, \"T1_bottom\": %ld, \"T2_top\": %ld, \"T2_bottom\": %ld }", d_t1_top, d_t1_bottom, d_t2_top, d_t2_bottom) // JSON packet

    client.publish("sensors/seat_hogging", payload);
    Serial.println(payload);
  }
}
