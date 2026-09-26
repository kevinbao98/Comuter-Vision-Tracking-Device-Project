#define MAX_BUFF_LEN 255 // Max amount of charaters to store in memory

char c;
char str[MAX_BUFF_LEN];
uint8_t idx = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  //Serial.println("Hello from ESP!");

  if(Serial.available() > 0 ) { // Run if there is any data available from serial port
    c = Serial.read(); // Read one byte
    
    if (c != '\n') { // Still reading
      str[idx++] = c; // Parse string byte (char) by byte
    } else { // Done reading
      str[idx] = '\0'; // Convert it to a string
      idx = 0;

      Serial.print("ESP Recieved: ");
      Serial.println(str);
    }
  }
}
