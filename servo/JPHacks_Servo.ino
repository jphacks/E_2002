#include <VarSpeedServo.h>

VarSpeedServo mg996r;
VarSpeedServo sg90;

unsigned char sign;
boolean flag = false;

void setup() {
  
  Serial.begin(9600);

  mg996r.attach(5);
  mg996r.write(90);
  delay(100);
  sg90.attach(6);
  sg90.write(0);
  delay(100);
  
//  Serial.println("Finish setting");
}

void loop() {

  if (Serial.available() > 0){
    sign = Serial.read();
    switch(sign){
      case 'm':
        flag = !flag;
        if (flag){
          movePos(0);
          Serial.println("Servo on");
        }else{
          movePos(90);
          Serial.println("Servo off");
        }
        break;
      default:
        Serial.println("Unknown code");
        break;
    }
  }
  if(flag){
    servoSweep();
  }
}

void movePos(int deg){
  mg996r.write(deg, 100, true);
}

void servoSweep(){
  sg90.write(180, 100, true);
  delay(1000);
  sg90.write(0, 100, true);
  delay(1000);
}
