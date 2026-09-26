const int vRX_PIN = 32;
const int vRY_PIN = 4;
const int SW_PIN = 2;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  // INPUT_PULLUP keeps pin HIGH until pressed.
  pinMode(SW_PIN, INPUT_PULLUP);
}

void loop() {
  // put your main code here, to run repeatedly:
  int xVal = analogRead(vRX_PIN);
  int yVal = analogRead(vRY_PIN);

  int buttonVal = digitalRead(SW_PIN);

  Serial.print("X: "); Serial.print(xVal);
  Serial.print(" | Y: "); Serial.print(yVal);
  Serial.print(" | Button: "); Serial.println(buttonVal);

  delay(100);
}
