#define datatotal 768
#define datatotaleach 1
#define readfrom 0
int analogIn = A1;
int digitalIn = 13;
bool before = false;
bool countstart = false;
bool countdata = false;
void setup() {
  Serial.begin(500000,SERIAL_8E2);
}
int loopcount = 0;
int comb = 0;
int last = 0;
int looploopcount = 0;
int looploopindex = 0;

int data[datatotal];
int eachdata[datatotaleach];
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
        comb = 0;
        if(loopcount>0)
          Serial.println(looploopcount);
        
      }
    }
  }
  
  int digitalValue = digitalRead(digitalIn);
    if(digitalValue) {//digitalValue is true
      before = true;
      if(countdata) {
          int sum=0;
          for(int _ = readfrom; _<looploopcount; _++){
            sum+=eachdata[_];
          }
          data[loopcount-1]=sum/(looploopcount-readfrom);
          // Serial.print(looploopcount);
          looploopcount = 0;
          countdata = false;
        }
    }else{ //measuring
      if(before) {// negedge digitalValue
        if (loopcount<datatotal) {
          before = false;
          
          
          // if(loopcount>0){
          //   Serial.print(',');
          //   Serial.println(data[loopcount-1]);
          // }
          // data[loopcount]= read;
          last = loopcount;
          loopcount++;
          countstart=true;
        }
      }else{
        if(countstart) {
          eachdata[looploopcount]=analogRead(analogIn);
          looploopcount++;
          if (looploopcount == datatotaleach) {
            countstart=false;
            countdata = true;
          }
        }
      }
    }
  } 
