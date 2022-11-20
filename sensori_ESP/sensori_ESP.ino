#include <ArduinoJson.h>
#include <HTTPClient.h>
#include <AddicoreRFID.h>
#include <Esp32WifiManager.h>
#include "DHT.h"
#include <Wire.h>
#include <MPU6050.h>

#define ID_BIN "plastic bin"
#define DHTPIN 23     // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11  //definisco di quale tipo di sensore DHT deve essere utilizzato
#define PIN_CO2 A0   // Analogical pin connected to the CO2 sensor
#define PINTrigger 9  // Trigger pin of ultrasonic sensor 
#define PINEcho 10  // Echo pin connected of ultrasonic sensor 
#define SERVER_ADDR "https://flask.gmichele.it/"


DHT dht(DHTPIN, DHTTYPE);
MPU6050 mpu;
HTTPClient http;
StaticJsonDocument<1024> jsonMsg;

const char* ssid = "IOT"; // Qui va inserito il nome della propria rete WiFi
const char* password = "ciaociao1";// Qui va inserita la password di rete

unsigned long timestamp;
// Pitch, Roll and Yaw values
int pitch = 0;
int roll = 0;
float yaw = 0;
String msg;

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
  pinMode(PINTrigger, OUTPUT);
  pinMode(PINEcho, INPUT);
  pinMode(PIN_CO2, INPUT);
  timestamp = millis();

  connectToWiFi();
  dht.begin();

  //inizializzazione accelerometro 
  Serial.println("Initialize MPU6050");
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  mpu.calibrateGyro();  // Calibrate gyroscope. The calibration must be at rest.
  mpu.setThreshold(1);  // Set threshold sensivity. Default 3.
  checkSettings();     // Check settings
}

void loop() {
  if(WiFi.status() == WL_CONNECTED){
    //DHT11
    // attendo qualche secondo affinchè il sensore si stabilizzi ed abbia il tempo di effettuare la lettura dei dati.
    if (millis() - timestamp > 2000) {
      int humidity = (int ) dht.readHumidity(); //readHumidity() restituisce un valore di tipo float.
      int temperature = (int) dht.readTemperature();  // Read temperature as Celsius (the default)
    
      // Check if any reads failed and exit early (to try again).
      if (isnan(humidity) || isnan(temperature)) {
        Serial.println(F("Failed to read from DHT sensor!"));
        //return;
      }

      //SENSORE ULTRASONICO
      digitalWrite(pinTrigger, LOW);  // imposta l'uscita del trigger LOW
      digitalWrite(pinTrigger, HIGH);  // imposta l'uscita del trigger HIGH per 10 microsecondi
      delayMicroseconds(10);
      digitalWrite(pinTrigger, LOW); // imposta l'uscita del trigger LOW
      int durata = pulseIn(pinEcho, HIGH); // calcolo del tempo attraverso il pin di echo
      int distanza = (int) durata/58.31;
      
      //SENSORE DI CO2
      int co2 = analogRead(A0);

      //ACCELEROMETRO
      Vector normAccel = mpu.readNormalizeAccel();
      Vector normGyro = mpu.readNormalizeGyro();
      pitch = -(atan2(normAccel.XAxis, sqrt(normAccel.YAxis * normAccel.YAxis + normAccel.ZAxis * normAccel.ZAxis)) * 180.0) / M_PI;
      roll = (atan2(normAccel.YAxis, normAccel.ZAxis) * 180.0) / M_PI;
      //Ignore the gyro if our angular velocity does not meet our threshold
      if (normGyro.ZAxis > 1 || normGyro.ZAxis < -1) {
        normGyro.ZAxis /= 100;
        yaw += normGyro.ZAxis;
      }
      //Keep our angle between 0-359 degrees
      if (yaw < 0){ yaw += 360;}
      else if (yaw > 359) { yaw -= 360; }

      //CREAZIONE DEL PACCHETTO
      jsonMsg["idbin"] = ID_BIN;
      jsonMsg["temperature"] = temperature;
      jsonMsg["humidity"] = humidity;
      jsonMsg["co2"] = co2;
      jsonMsg["riempimento"] = distanza;
      jsonMsg["pitch"] = pitch;
      jsonMsg["roll"] = roll;
      jsonMsg["yaw"] = yaw;
      
      serializeJson(jsonMsg, msg);
      Serial.println(msg);
      http.begin(String(SERVER_ADDR));
      http.addHeader("Content-Type", "application/json"); // Specify content-type header
      int respCode = http.POST(output);

      if(respCode > 0){
          String resp = http.getString(); 
          Serial.print(respCode);
      }else{
          Serial.print("Errore: ");
          Serial.println(respCode);
      }
      
      http.end();
      timestamp = millis();
    }
  }
  else{
    println("Errore di connessione");
  }
}

void checkSettings() {
  Serial.println();

  Serial.print(" * Sleep Mode:        ");
  Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");

  Serial.print(" * Clock Source:      ");
  switch (mpu.getClockSource()) {
    case MPU6050_CLOCK_KEEP_RESET:     Serial.println("Stops the clock and keeps the timing generator in reset"); break;
    case MPU6050_CLOCK_EXTERNAL_19MHZ: Serial.println("PLL with external 19.2MHz reference"); break;
    case MPU6050_CLOCK_EXTERNAL_32KHZ: Serial.println("PLL with external 32.768kHz reference"); break;
    case MPU6050_CLOCK_PLL_ZGYRO:      Serial.println("PLL with Z axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_YGYRO:      Serial.println("PLL with Y axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_XGYRO:      Serial.println("PLL with X axis gyroscope reference"); break;
    case MPU6050_CLOCK_INTERNAL_8MHZ:  Serial.println("Internal 8MHz oscillator"); break;
  }

  Serial.print(" * Gyroscope:         ");
  switch (mpu.getScale()) {
    case MPU6050_SCALE_2000DPS:        Serial.println("2000 dps"); break;
    case MPU6050_SCALE_1000DPS:        Serial.println("1000 dps"); break;
    case MPU6050_SCALE_500DPS:         Serial.println("500 dps"); break;
    case MPU6050_SCALE_250DPS:         Serial.println("250 dps"); break;
  }

  Serial.print(" * Gyroscope offsets: ");
  Serial.print(mpu.getGyroOffsetX());
  Serial.print(" / ");
  Serial.print(mpu.getGyroOffsetY());
  Serial.print(" / ");
  Serial.println(mpu.getGyroOffsetZ());

  Serial.println();
}