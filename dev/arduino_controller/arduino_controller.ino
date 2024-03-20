/*
arduino controller acquiring data from fpga by spi communication.
    

* @author Gyeongjun Chae(https://github.com/cka09191)
 */

#define datatotal 768
#include <SPI.h>
#include <Arduino.h>

uint8_t const ssFPGA = 10;
int digitalIn = 13;
bool before = false;// before: was the previous value of digitalIn true?
bool countstart = false;// countstart: is the program currently counting data?

void setup() {
  Serial.begin(115200,SERIAL_8E2);
  pinMode(ssFPGA, OUTPUT);
  digitalWrite(ssFPGA, 1);
  SPI.begin();
  while (!Serial) {
		    ; // wait
	}
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
      }else if(readValue=='d'){//start the counting
        digitalWrite(ssFPGA, 0);
        SPI.beginTransaction( SPISettings( 4000000, MSBFIRST, SPI_MODE3 ) );
        int received = SPI.transfer16(0xFFFF);
        SPI.endTransaction();
        digitalWrite(ssFPGA, 1);
        Serial.println(received);
      }else if(readValue=='g'){//stop the counting and get the data
        digitalWrite(ssFPGA, 0);
        SPI.beginTransaction( SPISettings( 4000000, MSBFIRST, SPI_MODE3 ) );
        int received = SPI.transfer16(0x0000);
        SPI.endTransaction();
        digitalWrite(ssFPGA, 1);
        Serial.println(received);
      }else if(readValue=='h'){
        
      }else if(readValue=='k'){
        
      }else if(readValue=='m'){
        
      }else if(readValue=='n'){
        
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
      if(countstart) {//stop counting if not stopped, and get the data

            digitalWrite(ssFPGA, 0);
            SPI.beginTransaction( SPISettings( 4000000, MSBFIRST, SPI_MODE3 ) );
            int received = SPI.transfer16(0x0000);//stop counting, received data is count
            digitalWrite(ssFPGA, 1);

            data[loopcount]=received;
            loopcount++;
            countstart = false;//because reset is true, there is no data counted
        }
    }else{
      if(before) {// negedge digitalValue, start measuring
        if (loopcount<datatotal) {//if loopcount is less than datatotal, start measuring, else, do nothing
          before = false;
          
          //TODO: send start signal to FPGA
          digitalWrite(ssFPGA, 0);
          SPI.beginTransaction( SPISettings( 4000000, MSBFIRST, SPI_MODE3 ) );
          int received = SPI.transfer16(0xFFFFF);//start counting, received data should 0
          digitalWrite(ssFPGA, 1);
          //TODO: record data
          countstart=true;
        }
      }
    }
  } 
