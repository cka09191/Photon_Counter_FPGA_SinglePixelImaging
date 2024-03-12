#define datatotal 768

int digitalIn = 13;
bool before = false;// before: was the previous value of digitalIn true?
bool countstart = false;// countstart: is the program currently counting data?
bool countdata = false; // countdata: is the program currently has data counted?

void setup() {
  Serial.begin(500000,SERIAL_8E2);
}

int loopcount = 0;
int comb = 0;
int measuring_time = 1000;
int misodata = 0;

int data[datatotal];
//TODO: Explain each command

void loop() {
  if(Serial.available()>0){
    int readValue = Serial.read();
    if(readValue!=-1) {
      if(readValue=='8'){
        loopcount=0;
      }else if(readValue=='7'){
        Serial.println(loopcount);
      }else if(readValue=='1'){
        if(comb<loopcount){
          Serial.println(data[comb]);
          comb++;
        }
      }else if(readValue=='2'){
        if(comb>0) {
          Serial.println(data[comb]);
          comb--;
        }
      }else if(readValue=='4'){
        comb = 0;
      }else if(readValue=='a'){
        for (int i = 0; i < loopcount; i++)
          Serial.println(data[i]);
      }else if(readValue=='b'){
        if(loopcount>0) {
            if(Serial.available()>0){
              measuring_time = Serial.parseInt();
            }
        }
        
      }
    }
  }
  //digitalValue : DMD Change Signal(DCS)
  //when DCS is positive, it means that DMD is flipping the mirror.
  //when DCS is positive edge, 
  //Pattern Cycle: period of time between DMD is flipping the mirror
  //Flipping Time: period of time that DMD is flipping the mirror(58us)
  //Ignore Time: ignore first fall time after flipping the mirror(not used in this code)

  int digitalValue = digitalRead(digitalIn);
    if(digitalValue) {//digitalValue is true
      before = true;
      if(countdata) {//stop counting
            //TODO: stop counting

            countdata = false;
            
        }
    }else{
      if(before) {// negedge digitalValue, start measuring, record previous data
        if (loopcount<datatotal) {//if loopcount is less than datatotal, start measuring, else, do nothing
          before = false;
          
          //TODO: send start signal to FPGA

          //TODO: record data

          loopcount++;
          countstart=true;
        }
      }
    }
  } 
