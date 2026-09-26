#include <ESP32Servo.h>
#include <WiFi.h>

// WiFi setup
const char* ssid = "NETGEAR78";
const char* password = "silkybutter584";
const int PORT = 8080;
WiFiServer server(PORT); // Instantiating network server object to listen for incoming TCP connection
// IPAddress staticIP(192, 168, 0, 196); // Requesting specific address to be mapped with the ES32D NodeMCU
// Servo setup
Servo myServo;
const int servo_pin = 18;
int current_speed = 90;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myServo.attach(servo_pin);
  myServo.write(current_speed);
  WiFi.begin(ssid, password);
  server.begin();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print("Connecting...\n\n");
  }
  Serial.print("ESP32D IP Address: "); Serial.println(WiFi.localIP());
}

int slew_rate(int current_speed, String target_speed) {
  /* Slew rate - the speed the servo motor can change its position.*/
  Serial.print("current_speed = "); Serial.println(current_speed);
  int step_rate = (current_speed < target_speed.toInt()) ? 10 : -10;
  current_speed = current_speed + step_rate;
  return current_speed;
}

void loop() {
  WiFiClient client = server.available(); // Checks for connected clients
  
  if (client) {
    while(client.connected()) {
      if (client.available()) {
        String target_speed = client.readStringUntil('\n');
        target_speed.trim();
        Serial.print("Recieved command: "); Serial.println(target_speed);
        if(target_speed.length() > 0) {
          while (current_speed != target_speed.toInt()) {
            current_speed = slew_rate(current_speed, target_speed);
            myServo.write(current_speed);
            delay(25);
          }
          Serial.print("current_speed = "); Serial.println(current_speed);
        }
      }
    }
  }
}
