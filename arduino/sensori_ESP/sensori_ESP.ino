#include <ArduinoJson.h>
#include <HTTPClient.h>
//#include <AddicoreRFID.h>
#include <Esp32WifiManager.h>
#include "DHT.h"
#include <Wire.h>
#include "I2Cdev.h"
#include "MPU6050.h"

#define ID_BIN "plastic bin"
#define DHTPIN 23     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11  //definisco di quale tipo di sensore DHT deve essere utilizzato
#define PIN_CO2 34   // Analogical pin connected to the CO2 sensor
#define PINTrigger 19  // Trigger pin of ultrasonic sensor 
#define PINEcho 18  // Echo pin connected of ultrasonic sensor 
#define altezza 50
#define SERVER_ADDR "https://flask.gmichele.it/"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

DHT dht(DHTPIN, DHTTYPE);
HTTPClient http;
StaticJsonDocument<1024> jsonMsg1, jsonMsg2, jsonMsg3;

const char* ssid = "AlessiaSaporita"; // Qui va inserito il nome della propria rete WiFi
const char* password = "altalena";// Qui va inserita la password di rete

unsigned long timestamp;
// Pitch, Roll and Yaw values
int pitch = 0;
int roll = 0;
float yaw = 0;

const int MPU_addr=0x68;
int16_t AcX, AcY, AcZ;
//int16_t GyX, GyY, GyZ;

String msg1, msg2, msg3;

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
  //pinMode(PINTrigger, OUTPUT);
  //pinMode(PINEcho, INPUT);
  //pinMode(PIN_CO2, INPUT);
  timestamp = millis();

  connectToWiFi();

  //inizializzazione DHT
  dht.begin();
  //inizializzazione accelerometro 
  #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
      Wire.begin();
  #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
      Fastwire::setup(400, true);
  #endif
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}
void loop() {
  if(WiFi.status() == WL_CONNECTED){
    //DHT11
    // attendo qualche secondo affinchè il sensore si stabilizzi ed abbia il tempo di effettuare la lettura dei dati.
    if (millis() - timestamp > 2000) {
      int humidity = (int) dht.readHumidity(); //readHumidity() restituisce un valore di tipo float.
      int temperature = (int) dht.readTemperature();  // Read temperature as Celsius (the default)
    
      // Check if any reads failed and exit early (to try again).
      if (isnan(humidity) || isnan(temperature)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        //return;
      }

      //SENSORE ULTRASONICO
      digitalWrite(PINTrigger, LOW);  // imposta l'uscita del trigger LOW
      digitalWrite(PINTrigger, HIGH);  // imposta l'uscita del trigger HIGH per 10 microsecondi
      delayMicroseconds(10);
      digitalWrite(PINTrigger, LOW); // imposta l'uscita del trigger LOW
      int durata = pulseIn(PINEcho, HIGH); // calcolo del tempo attraverso il pin di echo
      int distanza = durata / 58.31;
      
      //SENSORE DI CO2
      int co2 = analogRead(PIN_CO2);
    
      //ACCELEROMETRO
      Wire.beginTransmission(MPU_addr);
      Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
      Wire.endTransmission(false);
      Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
      AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
      AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
      AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
      /*
      GyX=Wire.read()<<8|Wire.read();  // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
      GyY=Wire.read()<<8|Wire.read();  // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
      GyZ=Wire.read()<<8|Wire.read();  // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
      */
      pitch = (atan2(AcX, sqrt(AcY * AcY + AcZ * AcZ)) * 180.0) / M_PI;
      roll = (atan2(AcY, sqrt(AcX * AcX + AcZ * AcZ)) * 180.0) / M_PI;
      yaw = (atan2(sqrt(AcX * AcX + AcZ * AcZ), AcZ) * 180.0) / M_PI;
      
      //CREAZIONE DEI PACCHETTI
      //pacchetto con i valori rilevati da salvare in db
      jsonMsg1["idbin"] = ID_BIN;
      jsonMsg1["temperature"] = temperature;
      jsonMsg1["humidity"] = humidity;
      jsonMsg1["riempimento"] = (altezza-distanza)/altezza;

      //pacchetto con i valori per controllare ed eventualmente segnalare ribaltamento
      jsonMsg1["idbin"] = ID_BIN;
      jsonMsg2["roll"] = roll; //0 gradi
      jsonMsg2["pitch"] = pitch;  //90 gradi
      jsonMsg2["yaw"] = yaw;  //90 gradi
      
      //pacchetto con il valore di co2 per controllare ed eventualmente segnalare incendio
      jsonMsg1["idbin"] = ID_BIN;
      jsonMsg3["co2"] = co2;
      
      serializeJson(jsonMsg1, msg1);
      serializeJson(jsonMsg2, msg2);
      serializeJson(jsonMsg3, msg3);
      Serial.println(msg1);
      Serial.println(msg2);
      Serial.println(msg3);

      httpPOSTJSON(String(SERVER_ADDR + 'database/additem/'), msg1);
      httpPOSTJSON(String(SERVER_ADDR + 'checkribaltamento/'), msg2);
      httpPOSTJSON(String(SERVER_ADDR + 'checkincendio/'), msg3);
      timestamp = millis();
    }
  }
  else{
    Serial.println("Errore di connessione");
  }
}

String httpPOSTJSON(String serverName, String msg) {
  http.begin(serverName);
  http.addHeader("Content-Type", "application/json"); // Specify content-type header
  int httpResponseCode = http.POST(msg); 
  
  if (httpResponseCode>0) {
    String resp = http.getString(); 
    Serial.print(httpResponseCode);
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

