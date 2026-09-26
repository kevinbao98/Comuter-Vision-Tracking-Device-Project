#include <ESP32Servo.h>

Servo myservo;  // create servo object to control a servo

// ESP32 Pins
const int potPin = 34;   // GPIO 34 (Analog ADC1_CH6)
const int servoPin = 18; // GPIO 18 (PWM capable pin)

int val;    // variable to read the value from the analog pin

void setup() {
  // Allow allocation of all timers for PWM
  ESP32PWM::allocateTimer(0);
  Serial.begin(115200);

  myservo.setPeriodHertz(50);    // standard 50 hz servo  
  myservo.attach(servoPin, 500, 2400); // attaches the servo pin with pulse widths
}

void loop() {
  val = analogRead(potPin);            // read the ESP32 potentiometer (0 to 4095)
  val = map(val, 0, 4095, 0, 180);     // scale it to use it with the servo (0 to 180)
  Serial.print("val = "); Serial.println(val);
  myservo.write(val);                  // set the servo position
  delay(15);                           // wait for the servo to reach the position
}