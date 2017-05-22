// Output
int redPin   = 11;   // Red LED,   connected to digital pin 9
int greenPin = 9;  // Green LED, connected to digital pin 10
int bluePin  = 10;  // Blue LED,  connected to digital pin 11


long int inByte; 
int wait = 10; //10ms

void setup()
{
  pinMode(redPin,   OUTPUT);   // sets the pins as output
  pinMode(greenPin, OUTPUT);   
  pinMode(bluePin,  OUTPUT);
  
  Serial.begin(9600); 
}


void outputColour(int red, int green, int blue) {
//  red = 120;
//  blue = 0;
//  green =0;
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue); 
     
}




int* getColour() {
  int* colour;
  int i;
  
  i = 0;
  
  //for some reason it only works if we put a dud value between the C and 
  // the R value
  while (i < 4)
  {
    if (Serial.available() > 0) {
        colour[i] = Serial.read();
        i++;
    }
  }
  
  return colour;
}

// Main program
void loop()
{
//outputColour(120,120,120);

  if (Serial.available() > 0) {
    // get incoming byte:
    inByte = Serial.read();
    
     if (inByte == 'C') {
        int* one;
      one =  getColour();
//      Serial.print(one);
      //1 2 3 not 0 1 2 due to the dud value
      outputColour(one[1],one[2],one[3]);
      
       
    } 
  }
  
  delay(wait);
}

