#include <Preferences.h>  // Include the Preferences library

// Define the H-bridge control pins
const int IN1 = 22;  // IN1 pin for MOTOR-A
const int IN2 = 21;  // IN2 pin for MOTOR-A
const int IN3 = 6;  // IN3 pin for MOTOR-B
const int IN4 = 7;   // IN4 pin for MOTOR-B

Preferences preferences;  // Create a Preferences object
String boardName = "";  // The board's name
const int NAME_LENGTH = 10;  // Length of the random name

void setup() {
  // Start Serial communication
  Serial.begin(460800);
  Serial.println("Send commands: MOTOR_A/MOTOR_B FORWARD/REVERSE/BRAKE/STANDBY followed by a PWM value (1-100).");

  // Set all the motor control pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Initialize Preferences
  preferences.begin("motor-control", false);  // "motor-control" is the namespace, false = RW mode

  // Check if the board already has a name stored in flash memory
  boardName = preferences.getString("boardName", "");  // Read the name, default is an empty string

  if (boardName == "") {
    // If no name exists, generate and store a new one
    boardName = generateRandomName(NAME_LENGTH);
    preferences.putString("boardName", boardName);  // Store the generated name in flash
    Serial.print("Generated new board name: ");
    Serial.println(boardName);
  } else {
    Serial.print("Board name: ");
    Serial.println(boardName);
  }
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');  // Read the command from the serial
    processCommand(command);
  }
}

void processCommand(String command) {
  command.trim(); // Clean up input command string

  // Check for name request command
  if (command == "GET_NAME") {
    Serial.print("Board Name: ");
    Serial.println(boardName);
    return;
  }

  String motor = command.substring(0, command.indexOf(' '));  // Extract motor identifier (MOTOR_A or MOTOR_B)
  
  // Extract action and PWM value
  int secondSpaceIndex = command.indexOf(' ', command.indexOf(' ') + 1);  // Find the second space
  String action;
  int pwmValue = 0;

  if (secondSpaceIndex != -1) {
    // If there is a second space, it means there is a PWM value provided
    action = command.substring(command.indexOf(' ') + 1, secondSpaceIndex);
    pwmValue = command.substring(secondSpaceIndex + 1).toInt();  // Extract PWM value
    pwmValue = map(pwmValue, 1, 100, 1, 255);  // Map PWM from 1-100 to 1-255 for analogWrite
  } else {
    // If there is no second space, it's likely BRAKE or STANDBY, so no PWM value
    action = command.substring(command.indexOf(' ') + 1);
  }

  // Control MOTOR-A
  if (motor == "MOTOR_A") {
    if (action == "FORWARD") {
      analogWrite(IN2, 0);  // Clear any previous PWM
      digitalWrite(IN2, LOW);  // Set IN2 to LOW to move forward
      analogWrite(IN1, pwmValue);
      Serial.print("MOTOR_A Forward ");
      Serial.println(pwmValue);
    } else if (action == "REVERSE") {
      analogWrite(IN1, 0);  // Clear any previous PWM
      digitalWrite(IN1, LOW);  // Set IN1 to LOW to move in reverse
      analogWrite(IN2, pwmValue);
      Serial.print("MOTOR_A Reverse ");
      Serial.println(pwmValue);
    } else if (action == "BRAKE") {
      analogWrite(IN1, 0);  // Clear previous analog writes
      analogWrite(IN2, 0);
      digitalWrite(IN1, HIGH);  // Set both HIGH to apply brake
      digitalWrite(IN2, HIGH);
      Serial.println("MOTOR_A Brake");
    } else if (action == "STANDBY") {
      analogWrite(IN1, 0);  // Clear previous analog writes
      analogWrite(IN2, 0);
      digitalWrite(IN1, LOW);  // Set both LOW to enter standby
      digitalWrite(IN2, LOW);
      Serial.println("MOTOR_A Standby");
    } else {
      Serial.println("Invalid action for MOTOR_A. Use FORWARD, REVERSE, BRAKE, or STANDBY.");
    }
  }
  
  // Control MOTOR-B
  else if (motor == "MOTOR_B") {
    if (action == "FORWARD") {
      analogWrite(IN4, 0);  // Clear any previous PWM
      digitalWrite(IN4, LOW);  // Set IN4 to LOW to move forward
      analogWrite(IN3, pwmValue);
      Serial.print("MOTOR_B Forward ");
      Serial.println(pwmValue);
    } else if (action == "REVERSE") {
      analogWrite(IN3, 0);  // Clear any previous PWM
      digitalWrite(IN3, LOW);  // Set IN3 to LOW to move in reverse
      analogWrite(IN4, pwmValue);
      Serial.print("MOTOR_B Reverse ");
      Serial.println(pwmValue);
    } else if (action == "BRAKE") {
      analogWrite(IN3, 0);  // Clear previous analog writes
      analogWrite(IN4, 0);
      digitalWrite(IN3, HIGH);  // Set both HIGH to apply brake
      digitalWrite(IN4, HIGH);
      Serial.println("MOTOR_B Brake");
    } else if (action == "STANDBY") {
      analogWrite(IN3, 0);  // Clear previous analog writes
      analogWrite(IN4, 0);
      digitalWrite(IN3, LOW);  // Set both LOW to enter standby
      digitalWrite(IN4, LOW);
      Serial.println("MOTOR_B Standby");
    } else {
      Serial.println("Invalid action for MOTOR_B. Use FORWARD, REVERSE, BRAKE, or STANDBY.");
    }
  }
  
  // Invalid motor command
  else {
    Serial.println("Invalid motor. Use MOTOR_A or MOTOR_B.");
  }
}

// Generate a random name of the given length
String generateRandomName(int length) {
  String charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  String randomName = "";
  for (int i = 0; i < length; i++) {
    randomName += charset[random(0, charset.length())];
  }
  return randomName;
}
