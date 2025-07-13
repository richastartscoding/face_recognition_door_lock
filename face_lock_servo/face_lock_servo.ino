#include <Servo.h>

Servo lockServo;
const int servoPin = 9;  // Change if needed
char command;

void setup() {
  Serial.begin(9600);
  lockServo.attach(servoPin);
  lockServo.write(0); // Locked position at start
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.read();

    if (command == 'o') { // Open door
      lockServo.write(90);
      Serial.println("Door opened");
    }
    else if (command == 'c') { // Close door
      lockServo.write(0);
      Serial.println("Door closed");
    }
  }
}
