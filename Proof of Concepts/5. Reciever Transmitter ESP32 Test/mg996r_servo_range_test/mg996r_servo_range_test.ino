// Example: https://github.com/madhephaestus/ESP32Servo
#include <ESP32Servo.h>

const int servo_pin = 18;
const int VRx_PIN = 32;
Servo myServo;

int min_VRx = 0;
int max_VRx = 4095;
int min_servo_speed = 0;
int max_servo_speed = 180; // 0 is max left speed, 90 is zero speed, 180 is max right speed

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  myServo.attach(servo_pin);
}

void loop() {
  // put your main code here, to run repeatedly:
  int VRx_value = analogRead(VRx_PIN);
  int servo_output;

  if (VRx_value >= 2300 && VRx_value <= 2700) { // Stop
    servo_output = 90;
    myServo.write(servo_output);
  } 
  else if (VRx_value < 2400) { // Max Left
    servo_output = 0;
    myServo.write(servo_output);
  } 
  else if (VRx_value > 2600) { // Max Right
    servo_output = 180;
    myServo.write(servo_output);
  }

  Serial.print("VRx_value: "); Serial.print(VRx_value);
  Serial.print(" | Servo Output: "); Serial.println(servo_output);
}
