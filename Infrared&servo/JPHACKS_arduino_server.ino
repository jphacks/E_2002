#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <Arduino_JSON.h>
#include <ESP32Servo.h> 

const uint16_t kIrLed = 33; //irled pinの設定

uint32_t led_on = 0xE730E916; //全灯(白)
uint32_t led_off = 0xE730D12E; //消灯
uint32_t tv_on_off = 0x2FD48B7; //TVのオン・オフ
uint32_t digital = 0x2FD5EA1; //地デジ
uint32_t bs = 0x2FD3EC1; //BS
uint32_t ch1 = 0x2FD807F;
uint32_t ch2 = 0x2FD40BF;
uint32_t ch3 = 0x2FDC03F;
uint32_t ch4 = 0x2FD20DF;
uint32_t ch5 = 0x2FDA05F;
uint32_t ch6 = 0x2FD609F;
uint32_t ch7 = 0x2FDE01F;
uint32_t ch8 = 0x2FD10EF;
uint32_t ch9 = 0x2FD906F;
uint32_t ch10 = 0x2FD50AF;
uint32_t ch11 = 0x2FDD02F;
uint32_t ch12 = 0x2FD30CF;
const int codelen = 583;
int tmp[codelen];
uint16_t ir_air[codelen];

unsigned char sign;
String message = "Initial Message";
String Readings;
boolean servo_flag = false;

const char* ssid = "Buffalo-G-59F4";
const char* password = "74aeffudxiudt";
//const char* ssid = "AirPort12594";
//const char* password = "3574567163731";
const char* serverName = "https://jphack-smarm.com/api/air_conditioner_options/";

int pos = 0;
int sg90_pin = 18;
int mg996r_pin = 19;
int minUs = 500;
int maxUs = 2400;

IRsend irsend(kIrLed);
WebServer server(80);
Servo sg90;
Servo mg996r;

void handleLedON(){
  Serial.println("led on");
  message = "LED ON";
  irsend.sendNEC(led_on);
  server.send(200, "text/plain", message);
}

void handleLedOFF(){
  Serial.println("led off");
  message = "LED OFF";
  irsend.sendNEC(led_off);
  server.send(200, "text/plain", message);
}

void handleTVON( ){
  Serial.println("tv on");
  message="TV ON";
  String broad = "None";
  String strch = "None";
  irsend.sendNEC(tv_on_off);
  for (uint8_t i=0; i<server.args(); i++){
    Serial.print(server.argName(i));
    Serial.print(":");
    Serial.println(server.arg(i));
  }
  broad = server.arg(0);
  strch = server.arg(1);
  delay(3000);
  changebroad(broad.charAt(0));
  delay(1000);
  changechannel(strch.toInt());
  message += ": broadcast ";
  message += broad;
  message += ": ch";
  message += strch;
  server.send(200, "text/plain", message);
}

void handleTVOFF(){
  Serial.println("tv off");
  message="TV OFF";
  irsend.sendNEC(tv_on_off);
  server.send(200, "text/plain", message);
}

void handleServo(){
  Serial.println("Control servo");
  message = "Control Servo";
  servo_flag = !servo_flag;
  if (servo_flag){
    mg996r.write(0);
    delay(100);
  }else{
    mg996r.write(90);
    delay(100);
  }
  server.send(200, "text/plain", message);
}

void handleAir(){
  Serial.println("control airconditioner");
  message="Control Airconditioner";
  Readings = httpGETRequest(serverName);
  JSONVar myArray = JSON.parse(Readings);
  if (JSON.typeof(myArray) == "undefined") {
    Serial.println("Parsing input failed!");
    return;
  }
  Serial.println(myArray.length());
  for (int i=0; i<myArray.length(); i++){
    tmp[i] = ( int)myArray[i];
    ir_air[i] = (uint16_t)tmp[i];
//    Serial.println(ir_air[i]);
  }
  irsend.sendRaw(ir_air, codelen, 38);
  server.send(200, "text/plain", message);
}

void setup() {
  
  sg90.setPeriodHertz(50); 
  sg90.attach(sg90_pin, minUs, maxUs);
  
  mg996r.setPeriodHertz(50); 
  mg996r.attach(mg996r_pin, minUs, maxUs);

  sg90.write(0);
  delay(100);
  mg996r.write(90);
  delay(100);
  
  irsend.begin();
  
  Serial.begin(115200);

  Serial.printf("Connecting to %s", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
  }
  Serial.println(" CONNECTED");

  server.on("/ledon", handleLedON);
  server.on("/ledoff", handleLedOFF);
  server.on("/tvon", handleTVON);
  server.on("/tvoff", handleTVOFF);
  server.on("/air", handleAir);
  server.on("/servo", handleServo);
  server.onNotFound([](){
    server.send(404, "text/plain", "Not Found."); // 404を返す
  });

  server.begin();

}

void loop() {

  server.handleClient();
  
  if (Serial.available() > 0){
    sign = Serial.read();
    switch(sign){
      case 'i':
        Serial.print("IP address: ");
        Serial.println( WiFi.localIP());
        break;
      }
   }
   if (servo_flag){
    sg90.write(0);
    delay(1000);
    sg90.write(180);
    delay(1000);
   }
}

void changebroad(char broad){
  uint32_t irdata = 0;
  switch (broad){
    case 'd':
      irdata = digital;
      break;
    case 'b':
      irdata = bs;
      break;
  }
  Serial.print("TV ir:");
  Serial.println(irdata, HEX);
  irsend.sendNEC(irdata);
}

void changechannel(int ch){
  uint32_t irdata = 0;
  switch (ch){
    case 1:
      irdata = ch1;
      break;
    case 2:
      irdata = ch2;
      break;
    case 3:
      irdata = ch3;
      break;
    case 4:
      irdata = ch4;
      break;
    case 5:
      irdata = ch5;
      break;
    case 6:
      irdata = ch6;
      break;
    case 7:
      irdata = ch7;
      break;
    case 8:
      irdata = ch8;
      break;
    case 9:
      irdata = ch9;
      break;
    case 10:
      irdata = ch10;
      break;
    case 11:
      irdata = ch11;
      break;
    case 12:
      irdata = ch12;
      break;
  }
  Serial.print("channel ir:");
  Serial.println(irdata, HEX);
  irsend.sendNEC(irdata);
}

String httpGETRequest(const char* serverName) {
  HTTPClient http;
    
  // Your IP address with path or Domain name with URL path 
  http.begin(serverName);
  
  // Send HTTP POST request
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
  // Free resources
  http.end();

  return payload;
}
