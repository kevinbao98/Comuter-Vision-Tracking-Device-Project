#include <WiFi.h>
#include <ESP32Servo.h>

// 1. Enter your Wi-Fi Credentials
const char* ssid     = "Invigatorium East";
const char* password = "Moose2017!?@";

// 2. Setup Server Port & Hardware Pins
const int PORT = 8080;
const int SERVO_PIN = 18; // GPIO pin connected to Servo signal line (PWM)

WiFiServer server(PORT); // Creating a server that listens to PORT. https://docs.arduino.cc/language-reference/en/functions/wifi/server/
Servo myServo;

void setup() {
  Serial.begin(115200);

  // Attach Servo to pin with standard pulse widths (500us to 2400us)
  // myServo.setPeriodHertz(50); // Standard 50Hz servo
  myServo.attach(SERVO_PIN, 500, 2400); 
  myServo.write(90); // Default center position

  // Connect to Wi-Fi
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi connected successfully!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP()); // <-- Copy this IP address into the Python script

  // Start TCP Server
  server.begin();
  Serial.printf("Server started on port %d\n", PORT);
}

int slew_rate(int current_speed, String target_speed) {
  /* Slew rate - the speed the servo motor can change its position.*/
  Serial.print("current_speed = "); Serial.println(current_speed);
  int step_rate = (current_speed < target_speed.toInt()) ? 10 : -10;
  current_speed = current_speed + step_rate;
  return current_speed;
}

void loop() {
  // Check for incoming TCP client connection from Python
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      if (client.available()) {
        // Read transmitted string until newline delimiter
        String input = client.readStringUntil('\n');
        input.trim();
        if (input.length() > 0) {
          int angle_speed = input.toInt();
          // Enter slew rate here
          myServo.write(angle_speed);

          Serial.printf("Received target angle speed: %d°\n", angle_speed);
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected.");
  }
}