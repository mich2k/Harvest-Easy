#include <SPI.h>
#include <MFRC522.h>
//#include <Servo.h> 
#include <Esp32WifiManager.h>
#include <stdlib.h>
#include <ArduinoJson.h>
#include <HTTPClient.h>

#define ID_BIN "plastic bin"
#define SERVER_ADDR "https://flask.gmichele.it/"
#define RST_PIN         22       //pin di reset    
#define SS_PIN          21       //pin di selezione

HTTPClient http;
StaticJsonDocument<1024> jsonMsg1, jsonMsg2, jsonMsg3;
String msg1, msg2, msg3;

//#define PIN_SERVO  3
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

String inStringDec = "";
String inStringHex = "";

//Servo servo; // servo object representing the MG 996R servo
MFRC522::Uid uid;
const char* ssid = "AlessiaSaporita"; // Qui va inserito il nome della propria rete WiFi
const char* password = "altalena";// Qui va inserita la password di rete
void connectToWiFi() {
    WiFi.begin(ssid, password); 
        while (WiFi.status() != WL_CONNECTED) {
                delay(2000); // 2 secondi prima di ritentare la connessione 
                Serial.println("Tentativo di connessione");
        }
        Serial.println("Connesso alla rete locale!");
}


void setup() {
  Serial.begin(9600); 
  connectToWiFi();
  //servo.attach(PIN_SERVO);
  while (!Serial);      // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
  SPI.begin();          // Init SPI bus
  mfrc522.PCD_Init();   //Init MRFC522
  mfrc522.PCD_DumpVersionToSerial();   // Show details of PCD - MFRC522 Card Reader details
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    // Look for new cards
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()){
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        inStringHex += String(mfrc522.uid.uidByte[i], HEX);
      }

      for (byte i = 0; i < mfrc522.uid.size; i++) {
        inStringDec += String(mfrc522.uid.uidByte[i], DEC);
      }
      Serial.println(F("Card UID_DEC:"));
      Serial.print(inStringDec);
      Serial.println();
      Serial.println(F("Card UID HEX:"));
      Serial.print(inStringHex);
      Serial.println();

      //CREAZIONE DEL PACCHETTO 
      //pacchetto con il valore di UID per controllare se l'utente ha disponibilità di accesso
      jsonMsg1["idbin"] = ID_BIN;
      jsonMsg1["UID"] = inStringDec;
      serializeJson(jsonMsg1, msg1);
      Serial.println(msg1);
      http.begin(String(SERVER_ADDR + 'database/checkUID'));
      http.addHeader("Content-Type", "application/json"); // Specify content-type header
      int respCode1 = http.POST(msg1);
      checkrisp(respCode1);
      http.end();
      
      inStringHex = "";
      inStringDec = "";
    }
  }
}

void checkrisp(int respCode){
  //se utente corretto e status non pieno devo aprire il bidone
  //delay(50000); //attendo un po prima di tornare ad aprire bidone
  
  if(respCode > 0){
      String resp = http.getString(); 
      Serial.print(respCode);
    }else{
      Serial.print("Errore: ");
      Serial.println(respCode);
    }
}
