static const int MESSAGE_LENGTH = 24; //standard format should be: PWR9-COM9-COD9-SBY9-AUX0
static const int COMMAND_LENGTH = 4; //3 chars and 1 integer
static const char SEPERATOR = '-';

static const int OUT_TESTING_PIN = 9;

void setup() {
  pinMode(OUT_TESTING_PIN, OUTPUT);
  
  Serial.begin(9600);
  Serial.setTimeout(500);
  
  while(!Serial){
    //wait for connection
  }
  
  Serial.println("established");
}

void loop() {
  if(Serial.available() > 0){
    String command = Serial.readString(); //standard format should be: PWR9-COM9-COD9-SBY9-AUX0
    if(command.length() != MESSAGE_LENGTH){ //bad format == data loss
      clearSerial();
      return;
    }
    
    int counter = 0; //error checking
    int statusInfo[5]; //extracted ints
    
    for(int i = COMMAND_LENGTH; i < MESSAGE_LENGTH - COMMAND_LENGTH; i += COMMAND_LENGTH + 1){
      if(command.charAt(i) == '-'){
        counter++;
        statusInfo[(i-COMMAND_LENGTH)/(COMMAND_LENGTH+1)] = command.charAt(i-1)-48;
      }
    }
    
    statusInfo[4] = command.substring(23).toInt()-48;
    
    if(counter != 4){
      clearSerial();
      return;
    }

    //
    //do stuff here with statusInfo which contains information about everything
    //
    
    if(statusInfo[0] > 5){
      digitalWrite(OUT_TESTING_PIN, HIGH);
    } else{
      digitalWrite(OUT_TESTING_PIN, LOW);
    }
    
    clearSerial(); //just to be safe
  }
}

void clearSerial(){
  while(Serial.available() > 0){
    Serial.read();
  }
}

