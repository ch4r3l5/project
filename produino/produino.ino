char val; // Data received from the serial port
 int redPin = 11; // Set the pin to digital I/O 13
int greenPin = 9;
int bluePin = 10;

 void setup() {
   pinMode(redPin, OUTPUT); // Set pin as OUTPUT
   pinMode(greenPin, OUTPUT); // Set pin as OUTPUT
   pinMode(bluePin, OUTPUT); // Set pin as OUTPUT
   Serial.begin(9600); // Start serial communication at 9600 bps
 }


  void loop() {
   if (Serial.available()) 
   { // If data is available to read,
     val = Serial.read(); // read it and store it in val
   }

   
  
   if (val == '1') 
   { // If 1 was received
     digitalWrite(redPin, 0); // turn the LED on
     digitalWrite(greenPin, 255); // turn the LED on
     digitalWrite(bluePin, 0); // turn the LED on
   } else {
     digitalWrite(redPin, LOW); // otherwise turn it off
     digitalWrite(greenPin, LOW); // otherwise turn it off
     digitalWrite(bluePin, LOW); // otherwise turn it off
   }
   delay(10); // Wait 10 milliseconds for next reading


    if (val == '0') 
   { // If 1 was received
     digitalWrite(redPin, 102); // turn the LED on
     digitalWrite(greenPin, 51); // turn the LED on
     digitalWrite(bluePin, 0); // turn the LED on
   } else {
     digitalWrite(redPin, LOW); // otherwise turn it off
     digitalWrite(greenPin, LOW); // otherwise turn it off
     digitalWrite(bluePin, LOW); // otherwise turn it off
   }
   delay(10); // Wait 10 milliseconds for next reading
}
