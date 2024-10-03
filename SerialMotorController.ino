#include <Preferences.h>
#include <WiFi.h>
#include <ESPmDNS.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOU_PASSWORD";

// Define the H-bridge control pins
const int IN1 = 22;  // IN1 pin for MOTOR-A
const int IN2 = 21;  // IN2 pin for MOTOR-A
const int IN3 = 6;   // IN3 pin for MOTOR-B
const int IN4 = 7;   // IN4 pin for MOTOR-B

Preferences preferences;  // Create a Preferences object
String boardName = "";    // The board's name
const int NAME_LENGTH = 10;  // Length of the random name

WiFiServer server(80);  // Create a server on port 80

void setup() {
  Serial.begin(460800);  // Changed to a more common baud rate
  while (!Serial) {
    ; // Wait for serial port to connect. Needed for native USB port only
  }
  Serial.println("Initializing...");

  // Set all the motor control pins as outputs
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Set the built-in LED pin as an output
  pinMode(LED_BUILTIN, OUTPUT);

  analogWrite(IN1, 0);
  analogWrite(IN2, 0);
  analogWrite(IN3, 0);
  analogWrite(IN4, 0);
  
  // Initialize Preferences
  preferences.begin("motor-control", false);

  // Check if the board already has a name stored in flash memory
  boardName = preferences.getString("boardName", "");

  if (boardName == "") {
    boardName = generateRandomName(NAME_LENGTH);
    preferences.putString("boardName", boardName);
    Serial.print("Generated new board name: ");
    Serial.println(boardName);
  } else {
    Serial.print("Board name: ");
    Serial.println(boardName);
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
    digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  digitalWrite(LED_BUILTIN, HIGH);

  // Start mDNS responder
  if (!MDNS.begin(boardName.c_str())) {
    Serial.println("Error setting up mDNS responder!");
  } else {
    Serial.println("mDNS responder started");
    MDNS.addService("http", "tcp", 80);
  }

  // Start the server
  server.begin();
  Serial.println("Server started");
}

void loop() {
  // Check WiFi connection status
  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("WiFi disconnected. Attempting to reconnect...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
    Serial.println("Reconnected to WiFi");
    digitalWrite(LED_BUILTIN, HIGH);
  }

  // Check for incoming serial commands
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    String result = processCommand(command);
    Serial.println(result);
  }

  // Check for incoming WiFi clients
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    while (client.connected()) {
      if (client.available()) {
        String command = client.readStringUntil('\n');
        command.trim();
        String result = processCommand(command);
        client.println(result);
        Serial.println("Sent to client: " + result);
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}

String processCommand(String command) {
  command.trim();

  if (command == "GET_NAME") {
    return "Board Name: " + boardName;
  }

  String motor = command.substring(0, command.indexOf(' '));
  
  int secondSpaceIndex = command.indexOf(' ', command.indexOf(' ') + 1);
  String action;
  int pwmValue = 0;

  if (secondSpaceIndex != -1) {
    action = command.substring(command.indexOf(' ') + 1, secondSpaceIndex);
    pwmValue = command.substring(secondSpaceIndex + 1).toInt();
    pwmValue = map(pwmValue, 1, 100, 1, 255);
  } else {
    action = command.substring(command.indexOf(' ') + 1);
  }

  String result = "";

  // Control MOTOR-A
  if (motor == "MOTOR_A") {
    if (action == "FORWARD") {
      analogWrite(IN2, 0);
      digitalWrite(IN2, LOW);
      analogWrite(IN1, pwmValue);
      result = "MOTOR_A Forward " + String(pwmValue);
    } else if (action == "REVERSE") {
      analogWrite(IN1, 0);
      digitalWrite(IN1, LOW);
      analogWrite(IN2, pwmValue);
      result = "MOTOR_A Reverse " + String(pwmValue);
    } else if (action == "BRAKE") {
      analogWrite(IN1, 0);
      analogWrite(IN2, 0);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, HIGH);
      result = "MOTOR_A Brake";
    } else if (action == "STANDBY") {
      analogWrite(IN1, 0);
      analogWrite(IN2, 0);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      result = "MOTOR_A Standby";
    } else {
      result = "Invalid action for MOTOR_A. Use FORWARD, REVERSE, BRAKE, or STANDBY.";
    }
  }
  
  // Control MOTOR-B
  else if (motor == "MOTOR_B") {
    if (action == "FORWARD") {
      analogWrite(IN4, 0);
      digitalWrite(IN4, LOW);
      analogWrite(IN3, pwmValue);
      result = "MOTOR_B Forward " + String(pwmValue);
    } else if (action == "REVERSE") {
      analogWrite(IN3, 0);
      digitalWrite(IN3, LOW);
      analogWrite(IN4, pwmValue);
      result = "MOTOR_B Reverse " + String(pwmValue);
    } else if (action == "BRAKE") {
      analogWrite(IN3, 0);
      analogWrite(IN4, 0);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, HIGH);
      result = "MOTOR_B Brake";
    } else if (action == "STANDBY") {
      analogWrite(IN3, 0);
      analogWrite(IN4, 0);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      result = "MOTOR_B Standby";
    } else {
      result = "Invalid action for MOTOR_B. Use FORWARD, REVERSE, BRAKE, or STANDBY.";
    }
  }
  
  else {
    result = "Invalid motor. Use MOTOR_A or MOTOR_B.";
  }

  return result;
}

String generateRandomName(int length) {
  String charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  String randomName = "";
  for (int i = 0; i < length; i++) {
    randomName += charset[random(0, charset.length())];
  }
  return randomName;
}