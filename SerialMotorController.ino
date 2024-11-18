#include <Preferences.h>
#include <WiFi.h>
#include <ESPmDNS.h>

String ssid = "DEFAULT_SSID";
String password = "DEFAULT_PASSWORD";

// This is a commandBuffer FIFO style.
// If a new command comes in before all the old commands are popped off
// and there is no more space.  The older commands will get dropped.
String commandQueue[100];
int queueStart = 0;
int queueEnd = 0;

void pushCommand(String command) {

  if ((queueEnd + 1) % 100 == queueStart) {
    // Queue is full, drop the oldest command
    queueStart = (queueStart + 1) % 100;
  }
  commandQueue[queueEnd] = command;
  queueEnd = (queueEnd + 1) % 100;
}

String popCommand() {
  if (queueStart == queueEnd) {
    // Queue is empty
    return "";
  }
  String command = commandQueue[queueStart];
  queueStart = (queueStart + 1) % 100;
  return command;
}

int peekCommandCount() {
  if (queueEnd >= queueStart) {
    return queueEnd - queueStart;
  } else {
    return 100 - queueStart + queueEnd;
  }
}

// Define the H-bridge control pins
const int IN1 = 22;  // IN1 pin for MOTOR-A
const int IN2 = 21;  // IN2 pin for MOTOR-A
const int IN3 = 6;   // IN3 pin for MOTOR-B
const int IN4 = 7;   // IN4 pin for MOTOR-B

Preferences preferences;  // Create a Preferences object
String boardName = "";    // The board's name
const int NAME_LENGTH = 10;  // Length of the random name

WiFiServer server(80);  // Create a server on port 80

bool useWiFi = false;  // Flag to enable/disable WiFi functionality

void setup() {
  Serial.begin(460800);
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

  // Load WiFi credentials from preferences
  ssid = preferences.getString("ssid", ssid);
  password = preferences.getString("password", password);

  // Check if WiFi should be enabled (stored in preferences)
  useWiFi = preferences.getBool("useWiFi", false);
  Serial.print("WiFi is ");
  Serial.println(useWiFi ? "enabled" : "disabled");

  if (useWiFi) {
    initializeWiFi();
  }

  Serial.println("Setup complete. Type 'HELP' for available commands.");
}

void loop() {
  if (useWiFi) {
    handleWiFi();
  }

  // Check for serial input
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    pushCommand(command);
  }

  // See if there are commands to pull off the queue
  String res = checkStack();
  if (res.length() > 0) {
    Serial.println(res);
  }
}

String checkStack() {
  if (peekCommandCount() > 0) {
    String command = popCommand();
    String result = processCommand(command);
    return result;
  }
  return "";
}

void initializeWiFi() {
  // Connect to Wi-Fi
  WiFi.begin(ssid.c_str(), password.c_str());
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
    MDNS.addService("motor", "tcp", 80);
  }

  // Start the server
  server.begin();
  Serial.println("Server started");
}

void handleWiFi() {
  // Check WiFi connection status
  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("WiFi disconnected. Attempting to reconnect...");
    WiFi.begin(ssid.c_str(), password.c_str());
    while (WiFi.status() != WL_CONNECTED) {
      delay(1000);
      digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));
    }
    Serial.println("Reconnected to WiFi");
    digitalWrite(LED_BUILTIN, HIGH);
  }

  // Check for incoming WiFi clients
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New client connected");
    while (client.connected()) {
      while (client.available()) {
        String command = client.readStringUntil('\n');
        command.trim();
        pushCommand(command);
      }

      while (peekCommandCount() > 0) {
        client.println(checkStack());
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}

String processCommand(String command) {
  command.trim();

  if (command == "HELP" || command == "?") {
    return getHelpText();
  } else if (command == "GET_NAME") {
    return "Board Name: " + boardName;
  } else if (command.startsWith("SET_NAME ")) {
    String newName = command.substring(9); // "SET_NAME " is 9 characters
    if (isValidMDNSName(newName)) {
      boardName = newName;
      preferences.putString("boardName", boardName);
      if (useWiFi) {
        // Restart mDNS with new name
        MDNS.end();
        if (!MDNS.begin(boardName.c_str())) {
          return "Error setting up mDNS responder with new name!";
        }
        MDNS.addService("motor", "tcp", 80);
      }
      return "Board name updated to: " + boardName;
    } else {
      return "Invalid board name. Use only letters, numbers, and hyphens. Don't start or end with a hyphen. Max length is 63 characters.";
    }
  } else if (command == "WIFI_ON") {
    if (!useWiFi) {
      useWiFi = true;
      preferences.putBool("useWiFi", true);
      initializeWiFi();
      return "WiFi enabled and initialized";
    }
    return "WiFi is already enabled";
  } else if (command == "WIFI_OFF") {
    if (useWiFi) {
      useWiFi = false;
      preferences.putBool("useWiFi", false);
      WiFi.disconnect(true);
      WiFi.mode(WIFI_OFF);
      return "WiFi disabled";
    }
    return "WiFi is already disabled";
  } else if (command == "WIFI_STATUS") {
    return useWiFi ? "WiFi is enabled" : "WiFi is disabled";
  } else if (command.startsWith("SET_WIFI ")) {
    int firstSpace = command.indexOf(' ');
    int secondSpace = command.indexOf(' ', firstSpace + 1);
    if (secondSpace == -1) {
      return "Invalid SET_WIFI command. Use format: SET_WIFI SSID PASSWORD";
    }
    String newSSID = command.substring(firstSpace + 1, secondSpace);
    String newPassword = command.substring(secondSpace + 1);
    ssid = newSSID;
    password = newPassword;
    preferences.putString("ssid", ssid);
    preferences.putString("password", password);
    return "WiFi credentials updated. SSID: " + ssid;
  } else if (command == "GET_WIFI") {
    return "Current SSID: " + ssid;
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

String getHelpText() {
  String helpText = "Available commands:\n\n";
  helpText += "HELP or ?                    : Show this help message\n";
  helpText += "GET_NAME                     : Get the current board name\n";
  helpText += "SET_NAME <name>              : Set a new board name (letters, numbers, hyphens only)\n";
  helpText += "WIFI_ON                      : Enable WiFi\n";
  helpText += "WIFI_OFF                     : Disable WiFi\n";
  helpText += "WIFI_STATUS                  : Check WiFi status\n";
  helpText += "SET_WIFI <ssid> <password>   : Set WiFi credentials\n";
  helpText += "GET_WIFI                     : Get current WiFi SSID\n";
  helpText += "MOTOR_A <action> [<pwm>]     : Control Motor A\n";
  helpText += "MOTOR_B <action> [<pwm>]     : Control Motor B\n\n";
  helpText += "Motor actions:\n";
  helpText += "  FORWARD <pwm>  : Move forward (PWM: 1-100)\n";
  helpText += "  REVERSE <pwm>  : Move in reverse (PWM: 1-100)\n";
  helpText += "  BRAKE          : Apply brake\n";
  helpText += "  STANDBY        : Enter standby mode\n";
  return helpText;
}

String generateRandomName(int length) {
  String charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  String randomName = "";
  for (int i = 0; i < length; i++) {
    if (i == 0) {
      // Ensure the first character is a letter
      randomName += charset[random(0, 26)];
    } else {
      randomName += charset[random(0, charset.length())];
    }
  }
  return randomName;
}

bool isValidMDNSName(const String& name) {
  if (name.length() == 0 || name.length() > 63) {
    return false;
  }
  
  for (int i = 0; i < name.length(); i++) {
    char c = name.charAt(i);
    if (!(isalnum(c) || c == '-') || (i == 0 && c == '-') || (i == name.length() - 1 && c == '-')) {
      return false;
    }
  }
  
  return true;
}
