#include <ESP32Servo.h>
#include <ArduinoJson.h>
#include <Arduino_JSON.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Esp32WifiManager.h>
#include <stdlib.h>
#include <LiquidCrystal_I2C.h>
#include <string.h>
#include <Wire.h>
#include <HTTPClient.h>



#define ID_BIN 9
#define SERVER_ADDR "https://flask.gmichele.it/"
#define RST_PIN 25       //pin di reset  
#define SCK 18
#define MISO 19
#define MOSI 23
#define SDA 21
#define SERVO_PIN 26
#define BTN_PIN 12

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

MFRC522 mfrc522(33, RST_PIN);   

String inStringDec = "";
String inStringHex = "";

MFRC522::Uid uid;

LiquidCrystal_I2C lcd(0x27, 16, 2);

Servo servoMotor;
int buttonState = 0;
int flag_vis = 0;
unsigned long lastTime = 0;
unsigned long timerDelay = 3600000;
unsigned long fDelay = 4000;
unsigned long fLastTime = 0;
String sensorReadings;

const char* ssid = "IOT"; // Qui va inserito il nome della propria rete WiFi
const char* password = "ciaociao1";// Qui va inserita la password di rete

void connectToWiFi() {
  WiFi.disconnect();
  WiFi.begin(ssid, password); 
  while (WiFi.status() != WL_CONNECTED) {
        if ((millis() - fLastTime) > fDelay) {
            break;
        }
          delay(1000); // 2 secondi prima di ritentare la connessione 
          Serial.println("Tentativo di connessione");
          Serial.println(WiFi.status());
  }
  if(WiFi.status() == WL_CONNECTED){
  Serial.println("Connesso alla rete locale!");
  }
}


void setup() {
  Serial.begin(9600); 
  connectToWiFi();
  while (!Serial);
  servoMotor.attach(SERVO_PIN);      
  lcd.init();
  lcd.clear();         
  lcd.backlight();
  pinMode(BTN_PIN, INPUT);
  visualizza(90);
  SPI.begin();          // Init SPI bus
  mfrc522.PCD_Init();   //Init MRFC522
  mfrc522.PCD_DumpVersionToSerial();   // Show details of PCD - MFRC522 Card Reader details
  Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
	//RFID
    buttonState = digitalRead(BTN_PIN);
    // Utente prova ad aprire il bidone
    if(mfrc522.PICC_IsNewCardPresent()){
      for(int n = 0; n < 50000; n++){
      Serial.println("OK1");

      }
    }
    if(mfrc522.PICC_ReadCardSerial()){
            for(int n = 0; n < 50000; n++){
      Serial.println("OK2");
            }
    }
    if (buttonState == HIGH || (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial())){
      Serial.println("Entrato nell nfc"); 
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        inStringHex += String(mfrc522.uid.uidByte[i], HEX);
      }


      if(buttonState){
        Serial.println("BUTTON ON!");
        Serial.println(buttonState);
        inStringHex = "d3370a6";
        buttonState = LOW;
      }
    
      Serial.println(F("Card UID HEX:"));
      Serial.print(inStringHex);
      Serial.println();

      //controllare se l'utente ha disponibilità di accesso
      if(WiFi.status() == WL_CONNECTED){
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
      delay(2000);
      // Serial.println("nuova carta");
      mfrc522.PCD_Init();
      }else{
        checkrisp(200);
        delay(2000);
      }
    }else{
      Serial.println("Error status");
    }
  
  //AGGIORNO IL DISPLAY ogni 30 minuti
    if ((millis() - lastTime) > timerDelay) {
      visualizza(90);
      lastTime = millis();
    }
  }else{
    if(WiFi.status() != WL_CONNECTED){ // != 1

    if ((millis() - fLastTime) > fDelay) {

      buttonState = digitalRead(BTN_PIN);

      if(buttonState){
        Serial.println("BUTTON ON!");
        Serial.println(buttonState);
        // inStringHex = "d3370a6";
        buttonState = LOW;
        checkrisp(200); 
      }


      if ((millis() - lastTime) > timerDelay) {
      visualizza(90);
      lastTime = millis();
      }
      if(!flag_vis){
        flag_vis=1;
      visualizza(25);
      }
    fLastTime = millis();
     }
    }

      //AGGIORNO IL DISPLAY ogni 30 minuti

  }
}


void checkrisp(int respCode){

  if(respCode > 0){
      if(respCode == 200 or respCode==203){ //se utente è autorizzato e il bidone vuoto o se utente è un operatore
      Serial.println("dentro checkrisp con 200");
        lcd.setCursor(0,1);
        lcd.print("Autorizzato");
        //apro coperchio
        for (int pos = 0; pos <= 90; pos += 1) {
            servoMotor.write(pos);
            delay(15); // waits 15ms to reach the position
        }

        delay(30000); //attendo 2 minuti   120000

      //chiudo coperchio
        for (int pos = 90; pos >= 0; pos -= 1) {
            servoMotor.write(pos);
            delay(15); // waits 15ms to reach the position
        }

        delay(4000);

        visualizza(25);
        return;
      }

    if(respCode == 201){  //se utente è autorizzato ma il bidone è pieno
      lcd.setCursor(0,1);
      lcd.print("Autorizzato");
      
      delay(3000);
      //visualizzo appartamento più vicino
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
    
  }else{
    Serial.print("Errore: ");
    Serial.println(respCode);
    return;
  }
}

void visualizza(int batteria){
  if(WiFi.status() == WL_CONNECTED){
  String serverPath = "https://flask.gmichele.it/db/getrecord/" + String(ID_BIN);
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

  }else{
    if(WiFi.status() != WL_CONNECTED){ // != 1
    Serial.println("Fakone");
    String jsonString = "{\"riempimento\":0.01,\"status\":1,\"temperatura\":31}";

    myObject = JSON.parse(jsonString);
    }
  }
  
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


