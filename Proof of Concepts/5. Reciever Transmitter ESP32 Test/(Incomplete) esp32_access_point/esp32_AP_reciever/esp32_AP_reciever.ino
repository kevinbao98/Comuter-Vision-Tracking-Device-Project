#include <WiFi.h>
#include <ESP32Servo.h>

// Servo set up
Servo myServo;
const int servo_pin = 18;
int current_speed = 90;

// WiFi Server settings and initiation
const char* esp32_ssid = "ESP32-Direct-AP";
const char* esp32_password = "12345678password";
const int PORT = 8080;
WiFiServer server(PORT);

void setup() {
  Serial.begin(115200);
  // Setting Access Point information
  WiFi.softAP(esp32_ssid, esp32_password); // Returns IP address of AP interface  
  IPAddress esp32_IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(esp32_IP);

  myServo.attach(servo_pin);
  int pulseWidth = 1500;
  myServo.writeMicroseconds(pulseWidth);
  server.begin();
}

void slew_rate(int &current_speed, String target_speed) {
  /* Slew rate - max speed that the servo motor can change speed.*/
  // Round values down to the nearest 10th
  int step_rate = (current_speed < target_speed.toInt()) ? 10 : -10;
  while (current_speed != target_speed.toInt()) {
    Serial.print("current_speed = "); Serial.println(current_speed);
    current_speed = current_speed + step_rate;
    myServo.write(current_speed);
  }
  Serial.print("current_speed = "); Serial.println(current_speed);
  delay(25);
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) { 
        String target_speed = client.readStringUntil('\n'); // might want to change to int target_speed = client.parseInt()
        Serial.printf("ESP-32 Yaw: Recieved %s\n", target_speed);
        slew_rate(current_speed, target_speed);
      }
    }
  }
}