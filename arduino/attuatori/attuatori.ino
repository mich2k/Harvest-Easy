#include <ArduinoJson.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>
//#include <Servo.h> 
#include <Esp32WifiManager.h>
#include <stdlib.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>
#include <Wire.h>
#include <HTTPClient.h>

#define ID_BIN 1
#define SERVER_ADDR "https://flask.gmichele.it/"
#define RST_PIN         33       
#define SCK             18
#define MISO            19
#define MOSI            23
#define SDA             21


//ICONE
byte filling[8] = { 
  B01110,
  B11111,
  B00000,
  B11111,
  B11111,
  B11111,
  B11111,
  B11111
};

byte battery[8] = {
  B01110,
  B11111,
  B10001,
  B10101,
  B10101,
  B10101,
  B10001,
  B11111
};

byte percentuale[8] = {
  B00000,
  B00000,
  B01000,
  B00001,
  B00010,
  B00100,
  B01000,
  B10001
};

HTTPClient http;
StaticJsonDocument<1024> jsonMsg1;
JSONVar myObject;
String msg1, msg2;

//#define PIN_SERVO  3
MFRC522 mfrc522(SDA, RST_PIN);   // Create MFRC522 instance.

String inStringDec = "";
String inStringHex = "";

//Servo servo; // servo object representing the MG 996R servo
MFRC522::Uid uid;

LiquidCrystal_I2C lcd(0x27, 16, 2);


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
  while (!Serial);      
  lcd.init();
  lcd.clear();         
  lcd.backlight();
  visualizza(90);
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
      Serial.println(F("Card UID HEX:"));
      Serial.print(inStringHex);
      Serial.println();

    
      //controllare se l'utente ha disponibilità di accesso
      String serverPath= "https://flask.gmichele.it/check/checkuid/" + String(inStringHex) + "&" + String(ID_BIN);
      http.begin(serverPath.c_str());
      int respCode1 = http.GET();
      String risp = "{}"; 
      if (respCode1>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(respCode1);
        risp = http.getString();
      }
      else {
        Serial.print("Error code: ");
        Serial.println(respCode1);
      }
      http.end();
      myObject = JSON.parse(risp);
      Serial.print("JSON object = ");
      Serial.println(myObject);
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
      }
      int code = (int) myObject["code"];
      Serial.println(String(code));
      
      checkrisp(code); 
      http.end();

      inStringHex = "";
      inStringDec = "";
      delay(3000);
      Serial.println("nuova carta");
      mfrc522.PCD_Init();
    }
  
  //AGGIORNO IL DISPLAY ogni 30 minuti
    if ((millis() - lastTime) > timerDelay) {
      visualizza(90);
      lastTime = millis();
    }
  }
}


void checkrisp(int respCode){

  if(respCode > 0){ 
	  if(respCode == 200){ //se utente è autorizzato e il bidone vuoto
      lcd.setCursor(0,1);
      lcd.print("Autorizzato");
      //aziono il servo
      delay(4000);
      visualizza(90);
      return;
	  }

    if(respCode == 201){  //se utente è autorizzato ma il bidone è pieno 
      lcd.setCursor(0,1);
      lcd.print("Autorizzato");
      //visualizzo appartamento più vicino
      delay(3000);

      String serverPath = "https://flask.gmichele.it/neighbor/getneighbor/" + String(ID_BIN);
      http.begin(serverPath.c_str());
      Serial.println(serverPath.c_str());
      Serial.println("\n");
      int httpResponseCode = http.GET();
      String sensorReadings = "{}"; 
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        sensorReadings = http.getString();
      }
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }
      http.end();
      myObject = JSON.parse(sensorReadings);
      Serial.println(myObject);
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return;
      }
      String via = myObject["street"];
      int numero = (int) myObject["number"];
      Serial.print("via = ");
      Serial.println(via);
      Serial.print("numero = ");
      Serial.println(numero);
      String indirizzo = via + " " + String(numero);
      lcd.clear();
      lcd.setCursor(2,1);
      lcd.print(indirizzo);
      for (int positionCounter = 0; positionCounter < 10; positionCounter++) {
        lcd.scrollDisplayLeft();
        delay(500);
      }
      delay(2000);
      visualizza(90);      
      return;
	  }

    if(respCode == 202){  //se utente non è autorizzato 
      lcd.setCursor(0,1);
      lcd.print("Non autorizzato");
      delay(4000);
      visualizza(90);
      return;
    }

    if(respCode == 203){  //se utente è OPERATORE/ADMIN 
      lcd.setCursor(0,1);
      lcd.print("Autorizzato");
      //aziono il servo
      delay(4000);
      visualizza(90);
      return;
    }
    
  }else{
    Serial.print("Errore: ");
    Serial.println(respCode);
    return;
  }
}

void visualizza(int batteria){
  String serverPath = "https://flask.gmichele.it/get/getrecord/" + String(ID_BIN);
  http.begin(serverPath.c_str());
  int respCode2 = http.GET();
  String risp2 = "{}"; 
  if (respCode2>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(respCode2);
    risp2 = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(respCode2);
  }
  http.end();
  myObject = JSON.parse(risp2); //stato, temperatura, livello di riempimento
  Serial.print("JSON object = ");
  Serial.println(myObject);
  if (JSON.typeof(myObject) == "undefined") {
    Serial.println("Parsing input failed!");
    return;
  }
  String status="";
  int status_attuale = (int) myObject["status"]; //"Ready"; //status_attuale 
  if (status_attuale == 1)
    status="Disponibile";
  if (status_attuale == 2)
    status="Pieno";
  if (status_attuale == 3 || status_attuale == 4)
    status="Manomesso";
  int temperatura = (int) myObject["temperatura"];
  double riempimento = (double) myObject["riempimento"];  
  Serial.print("status_attuale = ");
  Serial.println(status_attuale);
  Serial.print("temperatura = ");
  Serial.println(temperatura);
  Serial.print("riempimento = ");
  Serial.println(riempimento);
  lcd.clear();
  delay(1000);
  lcd.createChar(1,filling);
  lcd.createChar(2,battery);
  lcd.setCursor(0,0);
  lcd.write(1);
  riempimento = (int)(riempimento*100);
  if (riempimento >= 10){
    lcd.print(String(riempimento));
  }
  else{
    lcd.setCursor(2,0);
    lcd.print(String(riempimento));
  }
  lcd.setCursor(3,0);
  lcd.print((char)37); //percentuale
  lcd.setCursor(4,0);
  lcd.print(" ");
  lcd.setCursor(5,0);
  lcd.write(2);
  lcd.print(String(batteria));
  lcd.setCursor(8,0);
  lcd.print((char)37); //percentuale

  lcd.setCursor(12,0);
  lcd.print(String(temperatura));
  lcd.setCursor(14,0);
  lcd.print((char)223); //grado
  lcd.setCursor(15,0);
  lcd.print((char)67); //celsius

  lcd.setCursor(0,1);
  lcd.print(status);
  return;
}


