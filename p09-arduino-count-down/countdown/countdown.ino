#include <stdio.h>
#include <string.h>
#include <SoftwareSerial.h>

#define RELAY1 4
#define RELAY2 5
#define RELAY3 6
#define RELAY4 7

SoftwareSerial bleSerial(2, 3); // RX, TX



// Main vars
int curTime = 0;
String relayStatus = "0000";
char sample[] = "0100;0000";


void setup() {
  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }

  // BLE configure
  bleSerial.begin(9600);
  
  // send an intro:
  Serial.println("Count down:");


  // internal led
  pinMode(LED_BUILTIN, OUTPUT);


  // all down
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(RELAY3, OUTPUT);
  pinMode(RELAY4, OUTPUT);

  relayStatus = "0000";
  updateGPIO(relayStatus);
}

void loop() {
  // Get a command
  if (Serial.available()) {
    inputParse(Serial.readString());
    Serial.println(String(curTime) + ";" + relayStatus);
    updateGPIO(relayStatus);
  }

  if (bleSerial.available()) {
    inputParse(bleSerial.readString());
    bleSerial.print(String(curTime) + ";" + relayStatus);
    updateGPIO(relayStatus);
  }


  if (curTime > 0) {
    delay(1000);
    curTime--;
    if (! curTime > 0) {
      relayStatus = "0000";
      updateGPIO(relayStatus);
    }
    #ifdef DEBUG    
    Serial.println(String(curTime) + ";" + relayStatus);
    #endif
  }


}


int inputParse(String input) {

  char delimiter[] = ";";
  char* ptr;
  char buf[sizeof(sample)];

  #ifdef DEBUG
  Serial.println(input);
  #endif

  //Asking for status
  if ((input == "STATUS") || (input == "S")) {
    return 0;
  }
  

  
  input.toCharArray(buf, sizeof(buf));

  // Get TimeOut
  ptr = strtok(buf, delimiter);
  if (ptr != NULL) {
    curTime = String(ptr).toInt();
    //Serial.println("Uptime: " + String(curTime));
  }

  // Get Gpio Status
  ptr = strtok (NULL, delimiter);
  if (ptr != NULL) {
    relayStatus = String(ptr);
    //Serial.println("Relay status: " + relayStatus);
  }

  // Sanity
  if (curTime <= 0) {
    curTime = 0;
    relayStatus = "0000";
  }


}


int updateGPIO(String status) {


  #ifdef DEBUG  
  bleSerial.print(status);
  Serial.println(status);
  #endif

  //if (relayStatus.length() != 4) {
  //  return(-1);
  //}  

  if (curTime > 0) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }

  // Relay 1
  if (status.charAt(0) == '1') {
    digitalWrite(RELAY1,0);
  } else {
    digitalWrite(RELAY1,1);
  }

  // Relay 2
  if (status.charAt(1) == '1') {
    digitalWrite(RELAY2,0);
  } else {
    digitalWrite(RELAY2,1);
  }

  // Relay 3
  if (status.charAt(2) == '1') {
    digitalWrite(RELAY3,0);
  } else {
    digitalWrite(RELAY3,1);
  }

  // Relay 4
  if (status.charAt(3) == '1') {
    digitalWrite(RELAY4,0);
  } else {
    digitalWrite(RELAY4,1);
  }


}

