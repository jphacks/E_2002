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


int x = 400;  // error 閾値
int y = 120; //  High prs / Low prs 閾値裕度

void setup(){
  Serial.begin(115200);
  for( int i=1; i<=4; i++){
    pinMode(i , INPUT);
  }
   pinMode(LED_BUILTIN, OUTPUT);
// Serial.println("OK");
}


void loop(){

  if(Serial.available() > 0 ){

   
    for(int i=0; i<9; i++ ){
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(100);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);
      delay(100);    
    } 
    
    unsigned char sign = Serial.read();

    if (sign =='g'){
      prs_sum = 0;
      prs_sum2 = 0;
      sleep_prs = 0;
      
      digitalWrite(LED_BUILTIN, HIGH);   // turn the LED on (HIGH is the voltage level)
      delay(1000);                       // wait for a second
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println(9); 
    }
    
    
    else if (sign == 's'){         // 圧力の初期値取得
      prs1 = analogRead(PRS_PIN1);
      prs2 = analogRead(PRS_PIN2);  
      prs3 = analogRead(PRS_PIN3);  
      prs4 = analogRead(PRS_PIN4);
    
      prs_sum = prs1 + prs2 + prs3 + prs4;
      Serial.println(prs_sum);
      //Serial.println(prs1);    
      // Serial.println(prs2); 
      // Serial.println(prs3);
      // Serial.println(prs4);
      //Serial.print("sum=");  
      //Serial.println(prs_sum);
    
      if(sleep_prs < prs_sum){
        sleep_prs = prs_sum;
      }
      //Serial.print("spres");
      //Serial.println(sleep_prs);
    }

    else if (sign == 'w'){  
      delay(300);
    
   //  Serial.println("W");
    //if(sleep_prs < x){ //初期値がx以下ならerror 
    //Serial.println("prs_sensor_Error");
    //
    
    
    
    
    }
    
    
     
     prs1 = analogRead(PRS_PIN1);
     prs2 = analogRead(PRS_PIN2);  
     prs3 = analogRead(PRS_PIN3);  
     prs4 = analogRead(PRS_PIN4);
     
     prs_sum2 = prs1 + prs2 + prs3 + prs4;
    
    // Serial.print("圧力合計=");           //test output
    // Serial.println(prs_sum2);
    // Serial.print("閾値=");
    // Serial.println(sleep_prs - y);
    
     if(prs_sum2 < 1400){     //圧力が(初期値-裕度)未満ならLOW
      Serial.println("0");     
     }
    
     else{
//      Serial.println(prs_sum2);
      Serial.println("1");                //圧力HIGH
     }
     
    }
  }
}
