#include <IRremote.h>

const int RECV_PIN = 2; //デジタルIOの11番ピンを受信データ入力用に設定
const int SEND_PIN = 3;

//uint32_t ON = 0xE73045BA; //オレンジ
uint32_t ON = 0xE730E916; //白色
uint32_t OFF = 0xE730D12E;
uint32_t Orange = 0xE730F10E;
uint32_t tv1 = 0x2FD48B7;
uint32_t tv2 = 0xC235C82D;
uint32_t v_up = 0x2FD58A7;
uint32_t v_down = 0x2FD7887;

unsigned char sign;

IRsend IrSender;
IRrecv IrReceiver(RECV_PIN);

void setup(){
  Serial.begin(9600);
  IrReceiver.enableIRIn();
  IrReceiver.blink13(true); 
//  Serial.println("finish setup");
}

void loop() {

  if (Serial.available()){
    sign = Serial.read();
    switch(sign){
      case 'a':
        Serial.println("Turn on the light");
        sendSignal(ON);
        break;
      case 'b':
        Serial.println("Turn off the light");
        sendSignal(OFF);
        break;
      case 'c':
        Serial.println("Turn on the orange light");
        sendSignal(Orange);
        break;
      case 'd':
        Serial.println("Turn on the TV");
        sendSignal(tv1);
        sendSignal(tv2);
        break;
      case 'e':
        Serial.println("Volume up");
        sendSignal(v_up);
        break;
      case 'f':
        Serial.println("Volume down");
        sendSignal(v_down);
        break;
      case 'r':
        Serial.println("Waiting IR data");
        readSignal();
        break;
      default:
        Serial.println("Unknown code");
        break;
    }
  }
}

void sendSignal(uint32_t sdata){
//  Serial.print("send :");
//  Serial.println(sdata, HEX);
  IrSender.sendNEC(sdata, 32);
}

void sendRawSignal(unsigned int irSignal[]){
  int khz = 38; // 38kHz carrier frequency for the NEC protocol
  IrSender.sendRaw(irSignal, sizeof(irSignal) / sizeof(irSignal[0]), khz); // Note the approach used to automatically calculate the size of the array.
}

void readSignal() {
  while(1){
    if (IrReceiver.decode()) {  // Grab an IR code
        dumpInfo();             // Output the results
        IrReceiver.printIRResultRawFormatted(&Serial);  // Output the results in RAW format
        Serial.println();                               // blank line between entries
        IrReceiver.printIRResultAsCArray(&Serial);      // Output the results as source code array
        IrReceiver.printIRResultAsCVariables(&Serial);  // Output address and data as source code variables
        IrReceiver.printIRResultAsPronto(&Serial);
        Serial.println();                               // 2 blank lines between entries
        Serial.println();
        IrReceiver.resume(); 
        break;
    }
  }
}
//+=============================================================================
// Dump out the decode_results structure.
//
void dumpInfo() {
    // Check if the buffer overflowed
    if (IrReceiver.results.overflow) {
        Serial.println("IR code too long. Edit IRremoteInt.h and increase RAW_BUFFER_LENGTH");
        return;
    }

    IrReceiver.printResultShort(&Serial);

    Serial.print(" (");
    Serial.print(IrReceiver.results.bits, DEC);
    Serial.println(" bits)");
}
