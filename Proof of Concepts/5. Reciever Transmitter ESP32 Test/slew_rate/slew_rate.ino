#include <ESP32Servo.h>

Servo myServo;
const int servo_pin = 18;
int current_speed = 90;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myServo.attach(servo_pin);
}

int slew_rate(int current_speed, String target_speed) {
  /* Slew rate - the speed the servo motor can change its position.*/
  Serial.print("current_speed = "); Serial.println(current_speed);
  int step_rate = (current_speed < target_speed.toInt()) ? 10 : -10;
  current_speed = current_speed + step_rate;
  return current_speed;
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available() > 0) {
    Serial.print("Enter servo speed: ");
    String target_speed = Serial.readString();
    Serial.println(target_speed);
    while (current_speed != target_speed.toInt()) {
      current_speed = slew_rate(current_speed, target_speed);
      myServo.write(current_speed);
      delay(25);
    }
    Serial.print("current_speed = "); Serial.println(current_speed);
  }
}
