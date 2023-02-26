#include <LiquidCrystal_I2C.h>
#include <Esp32WifiManager.h>
#include <stdlib.h>
#include <string.h>
#include <ArduinoJson.h>
#include <Arduino_JSON.h>
#include <HTTPClient.h>
#include <Wire.h>

#define ID_BIN 1
/*
LCD Pin – >ESP32 Pins

PIN01-VSS -> GND
PIN02-VDD -> 5V
PIN03 V0-> GND
PIN04 RS->  GPIO19
PIN05 RW-> GND
PIN06  E  ->  GPIO23
PIN07 D0-> NOT USED
PIN08 D1-> NOT USED
PIN09 D2-> NOT USED
PIN10 D3-> NOT USED
PIN11 D4->  GPIO18
PIN12 D5->  GPIO17
PIN13 D6->  GPIO16
PIN14 D7->  GPIO15
PIN15 A-> 5V
PIN16 K-> GND

*/
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
 
// Create An LCD Object. Signals: [ RS, EN, D4, D5, D6, D7 ]
//LiquidCrystal lcd(19, 23, 18, 17, 16, 15);
LiquidCrystal_I2C lcd(0x27, 16, 2);

unsigned long lastTime = 0;
unsigned long timerDelay = 3000; //60000; // 6 minuti //1800000 30 minuti
JSONVar myObject;
HTTPClient http;


void setup() {
  Serial.begin (9600);
  Serial.println ();
  Serial.println ("I2C scanner. Scanning ...");
  byte count = 0;
  
  Wire.begin();
  for (byte i = 8; i < 120; i++)
  {
    Wire.beginTransmission (i);
    if (Wire.endTransmission () == 0)
      {
      Serial.print ("Found address: ");
      Serial.print (i, DEC);
      Serial.print (" (0x");
      Serial.print (i, HEX);
      Serial.println (")");
      count++;
      delay (1);  // maybe unneeded?
      } // end of good response
  } // end of for loop
  Serial.println ("Done.");
  Serial.print ("Found ");
  Serial.print (count, DEC);
  Serial.println (" device(s).");
}  // end of setup

void loop() {}


/*
void setup() {
  Serial.begin(9600); 
  connectToWiFi();
  lcd.init();
  lcd.clear();         
  lcd.backlight();
  visualizza(90);
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){ 
    //AGGIORNO IL DISPLAY ogni 30 minuti
    if ((millis() - lastTime) > timerDelay) {
      visualizza(90);
      lastTime = millis();
    }
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
  }
  
  String status_attuale = "Ready"; //myObject["stato"]; //"Ready"; //status_attuale 
  int temperatura = (int) myObject["temperatura"];
  double riempimento = (double) myObject["riempimento"];  
  Serial.print("status_attuale = ");
  Serial.println(status_attuale);
  Serial.print("temperatura = ");
  Serial.println(temperatura);
  Serial.print("riempimento = ");
  Serial.println(riempimento);
  //lcd.clear();
  delay(1000);
  lcd.createChar(1,filling);
  lcd.createChar(2,battery);
  lcd.setCursor(0,0);
  lcd.write(1);
  lcd.print(String(riempimento*100));
  lcd.setCursor(3,0);
  lcd.print((char)37); //percentuale
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
  lcd.print(status_attuale);
  return;
}
*/

