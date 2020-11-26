const int PRS_PIN1 = 1;
const int PRS_PIN2 = 2;
const int PRS_PIN3 = 3;
const int PRS_PIN4 = 4;

int prs1 = 0;
int prs2 = 0;
int prs3 = 0;
int prs4 = 0;
int prs_sum = 0;
int prs_sum2 = 0;
int sleep_prs = 0;
int i;

int y = 120; //  High prs / Low prs 閾値裕度

void setup(){
  Serial.begin(115200);
  for( int i=1; i<=4; i++){
    pinMode(i , INPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
}


void loop(){

  if(Serial.available() > 0 ){
    
    unsigned char sign = Serial.read();

    if (sign =='g'){
      prs_sum = 0;
      prs_sum2 = 0;
      sleep_prs = 0;
      
      for(i=0; i<5; i++){
        digitalWrite(LED_BUILTIN, HIGH);  
        delay(100);                      
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
      }
      Serial.println("reset"); 
    }
    
    
    else if (sign == 's'){         // 圧力の初期値取得
      prs1 = analogRead(PRS_PIN1);
      prs2 = analogRead(PRS_PIN2);  
      prs3 = analogRead(PRS_PIN3);  
      prs4 = analogRead(PRS_PIN4);
    
      prs_sum = prs1 + prs2 + prs3 + prs4;
      Serial.print("Total pressure = ");
      Serial.println(prs_sum);

    
      if(sleep_prs < prs_sum){
        sleep_prs = prs_sum;
        for(i=0; i<2; i++){
          digitalWrite(LED_BUILTIN, HIGH);  
          delay(200);                      
          digitalWrite(LED_BUILTIN, LOW);
          delay(200);
          digitalWrite(LED_BUILTIN, HIGH);  
          delay(200);                      
          digitalWrite(LED_BUILTIN, LOW);
          delay(500);
       }
      }
    }

    else if (sign == 'w'){  
      delay(200);
     
      prs1 = analogRead(PRS_PIN1);
      prs2 = analogRead(PRS_PIN2);  
      prs3 = analogRead(PRS_PIN3);  
      prs4 = analogRead(PRS_PIN4);
     
      prs_sum2 = prs1 + prs2 + prs3 + prs4;
    
      if(prs_sum2 < sleep_prs - y){     //圧力が(初期値-裕度)未満ならLOW
        Serial.println("0");   
        for(i=0; i<3; i++){
          digitalWrite(LED_BUILTIN, HIGH);  
          delay(500);                      
          digitalWrite(LED_BUILTIN, LOW);
          delay(100);  
        }
      }
    
      else{                              //圧力HIGH
        Serial.println("1");    
          for(i=0; i<2; i++){
            digitalWrite(LED_BUILTIN, HIGH);  
            delay(1000);                      
            digitalWrite(LED_BUILTIN, LOW);
            delay(100);  
          }
        }
      }   
    }
  }
