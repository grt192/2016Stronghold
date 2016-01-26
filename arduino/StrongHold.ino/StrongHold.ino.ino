void setup() {
  Serial.begin(9600);
  Serial.setTimeout(500);
  
  while(!Serial){
    //wait for connection
  }
  
  Serial.println("established");
}

void loop() {
  if(Serial.available() > 0){
    String s = Serial.readString(); //standard format should be: PWR9-COM9-COD9-SBY9-AUX0

    if(s.length < 24){ //bad format
      clearSerial();
      return;
    }
    
    int counter = 0; //error checking
    int statusInfo[5];
    
    for(int i = 3; i <= 18; i = i + 5){
      if(s.charAt(i) == "-"){
        counter++;
        statusInfo[(i-3)/5] = s.charAt(i-1);
      }
    }

    String aux = s.substring(23);
    statusInfo[4] = aux.toInt();

    if(counter != 4){
      clearSerial();
      return;
    }

    //
    //do stuff here with statusInfo which contains information about everything
    //
    
    clearSerial(); //just to be safe
  }
}

void clearSerial(){
  while(Serial.available() > 0){
    Serial.read();
  }
}

