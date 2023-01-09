#include <ArduinoJson.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>
//#include <Servo.h> 
#include <Esp32WifiManager.h>
#include <stdlib.h>
#include <HTTPClient.h>

#define ID_BIN "plastic bin"
#define SERVER_ADDR "https://flask.gmichele.it/"
#define RST_PIN         22       //pin di reset    
#define SS_PIN          21       //pin di selezione

HTTPClient http;
StaticJsonDocument<1024> jsonMsg1;
JSONVar myObject;
String msg1, msg2, msg3;

//#define PIN_SERVO  3
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

String inStringDec = "";
String inStringHex = "";

//Servo servo; // servo object representing the MG 996R servo
MFRC522::Uid uid;

unsigned long lastTime = 0;
unsigned long timerDelay = 3600000;
String sensorReadings;

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
	//RFID
    // Utente prova ad aprire il bidone
    if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()){
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        inStringHex += String(mfrc522.uid.uidByte[i], HEX);
      }

      for (byte i = 0; i < mfrc522.uid.size; i++) {
        inStringDec += String(mfrc522.uid.uidByte[i], DEC);
      }
      Serial.println(F("Card UID DEC:"));
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

      //AGGIORNO IL DISPLAY ogni 30 minuti
    if ((millis() - lastTime) > timerDelay) {
      String serverPath = String(SERVER_ADDR) + 'database/getsensor?idbin='+ String(ID_BIN);
      sensorReadings = httpGETRequest(serverPath.c_str());
      myObject = JSON.parse(sensorReadings);
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
    
      Serial.print("JSON object = ");
      Serial.println(myObject);
      JSONVar keys = myObject.keys(); //stato, temperatura, livello di riempimento
      String status_attuale = myObject[keys[0]];
      int temperatura = int(myObject[keys[1]]);
      int riempimento = int(myObject[keys[2]]);

      Serial.print("status_attuale = ");
      Serial.println(status_attuale);
      Serial.print("temperatura = ");
      Serial.println(temperatura);
      Serial.print("riempimento = ");
      Serial.println(riempimento);
      lastTime = millis();
    }
  }
}


void checkrisp(int respCode){

  if(respCode > 0){ 
	  if(respCode == 200){ //se utente è autorizzato e il bidone vuoto
		//visualizzo "Autorizzato"
	  }

    if(respCode == 201){  //se utente è autorizzato ma il bidone è pieno 
      //visualizzo "autorizzato""
      //visualizzo bidone più vicino
      String serverPath = String(SERVER_ADDR) + 'neighbor/?idbin=' + String(ID_BIN);
      sensorReadings = httpGETRequest(serverPath.c_str());
      myObject = JSON.parse(sensorReadings);
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
        }
      JSONVar keys = myObject.keys(); //via, numero
      String via = myObject[keys[0]];
      int numero = int(myObject[keys[1]]);
      Serial.print("via = ");
      Serial.println(via);
      Serial.print("numero = ");
      Serial.println();
	  }

    if(respCode == 202){  //se utente non è autorizzato 
      //visualizzo "Non autorizzato"
    }

    if(respCode == 203){  //se utente è OPERATORE/ADMIN 
      //visualizzo "autorizzato"
      //aziono il servo
    }
    
  }else{
    Serial.print("Errore: ");
    Serial.println(respCode);
  }
}

String httpGETRequest(const char* serverName) {
  http.begin(serverName);
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
  return payload;
}