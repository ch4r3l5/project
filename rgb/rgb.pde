import processing.serial.*;

PImage img;  
Serial myPort;

void setup() {
  
  //set these to the size of the image
  size(512,512);
  
  //this is the name of your image file saved in the data folder in your
  //processing folder see processing.org for help
  
  img = loadImage("RGBR.png");
  
  //the [0] may be [another number] on your computer
  myPort = new Serial(this, Serial.list()[0], 9600);
  
}

void draw() {
  background(0);
  image(img,0,0);
  img.loadPixels();
}

void mousePressed() 
{
 println(Serial.list());
 myPort.write("CL");
 myPort.write(int(red(img.pixels[mouseX+mouseY*img.width])));
 myPort.write(int(green(img.pixels[mouseX+mouseY*img.width]))); 
 myPort.write(int(blue(img.pixels[mouseX+mouseY*img.width]))); 
 println(int(red(img.pixels[mouseX+mouseY*img.width])));
}
  