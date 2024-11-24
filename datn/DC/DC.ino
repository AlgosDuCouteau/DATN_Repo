/*
 * Created by ArduinoGetStarted.com
 *
 * This example code is in the public domain
 *
 * Tutorial page: https://arduinogetstarted.com/tutorials/arduino-joystick
 */

#include <ezButton.h>
ezButton toggleSwitch(8);

#define VRX_PIN  A0 // Arduino pin connected to VRX pin
#define VRY_PIN  A1 // Arduino pin connected to VRY pin
#define DB 5
#define PB 4
#define DA 2
#define PA 3

int xAxis = 517; // To store value of the X axis
int yAxis = 517; // To store value of the Y axis
int Count_pulses = 0;
int motorSpeedA = 0;
int motorSpeedB = 0;
int x;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  pinMode(VRX_PIN, INPUT);
  pinMode(VRY_PIN, INPUT);
  pinMode(DA, OUTPUT);
  pinMode(PA, OUTPUT);
  pinMode(DB, OUTPUT);
  pinMode(PB, OUTPUT);
  toggleSwitch.setDebounceTime(50);
}

void loop()
{ 
  //while (!Serial.available()) {};
  toggleSwitch.loop();
  int state = toggleSwitch.getState();
  if (state == LOW)
  {
    while (Serial.available() and state == LOW)
    {
      delay(30);
      x = Serial.readString().toInt();
      if (x == 0 or x == 4)
      {
        xAxis = 517;
        yAxis = 517;
      }
      else if (x == 1)
      {
        xAxis = 517;
        yAxis = 400;
      }
      else if (x == 2)
      {
        xAxis = 400;
        yAxis = 517;
      }
      else if (x == 3)
      {
        xAxis = 517;
        yAxis = 620;
      }
      else if (x == 5)
      {
        xAxis = 620;
        yAxis = 517;
      }
    }
  }
  else
  {
    xAxis = analogRead(VRX_PIN);
    yAxis = analogRead(VRY_PIN);
  }

  delay(100);

  // If joystick stays in middle the motors are not moving
  if (yAxis > 500 && yAxis <530 && xAxis > 500 && xAxis <530) Stop();
  
  if (yAxis > 500 && yAxis <530)
  {    
  // X-axis used for left and right control
    if (xAxis < 500)
    {
      turnLeft();
    // Convert the declining X-axis readings for going backward from 515 to 400 into 10 to 20 value for the PWM signal for increasing the motor speed  
      motorSpeedA = map(xAxis, 515, 400, 30, 60);
      motorSpeedB = map(xAxis, 515, 409, 30, 60);
    }
    
    if (xAxis > 530)
    {
      turnRight();
      // Convert the increasing X-axis readings for going forward from 515 to 621 into 10 to 20 value for the PWM signal for increasing the motor speed      
      motorSpeedA = map(xAxis, 515, 621, 30, 60);
      motorSpeedB = map(xAxis, 515, 621, 30, 60); 
    }
  }
  else
  {
    if (xAxis > 470 && xAxis <550)
    {   
    // Y-axis used for forward and backward control  
  
      if (yAxis < 500)
      {
        forword();
      // Convert the declining Y-axis readings for going backward from 515 to 400 into 10 to 20 value for the PWM signal for increasing the motor speed  
        motorSpeedA = map(yAxis, 515, 400, 30, 60);
        motorSpeedB = map(yAxis, 515, 400, 30, 60);
        
      }
      
      if (yAxis > 530)
      {
        backword();
      // Convert the increasing Y-axis readings for going forward from 515 to 625 into 10 to 20 value for the PWM signal for increasing the motor speed      
        motorSpeedA = map(yAxis, 515, 625, 30, 60);
        motorSpeedB = map(yAxis, 515, 625, 30, 60);
      }
     
    }
    else
    {
    
      if(yAxis < 500) forword();
      if(yAxis > 530) backword();
      
      if(xAxis < 500)
      {
        // Convert the declining X-axis readings from 515 to 400 into increasing 10 to 15 value
        int xMapped = map(xAxis, 515, 400, 10, 15);
        
        motorSpeedA = motorSpeedA - xMapped;
        motorSpeedB = motorSpeedB + xMapped;
        
        // Confine the range from 10 to 30
        if(motorSpeedB > 60) motorSpeedB = 60;
        if(motorSpeedA < 30) motorSpeedA = 30;
      }
       
      if (xAxis > 530)
      {
        // Convert the increasing X-axis readings from 515 to 625 into 10 to 15 value
        int xMapped = map(xAxis, 515, 625, 10, 15);
       
        motorSpeedA = motorSpeedA + xMapped;
        motorSpeedB = motorSpeedB - xMapped;
        
        // Confine the range from 10 to 30
        if(motorSpeedB < 30) motorSpeedB = 30;
        if(motorSpeedA > 60) motorSpeedA = 60;
      }
    }
  }
  
  // Prevent buzzing at low speeds (Adjust according to your motors. My motors couldn't start moving if PWM value was below value of 70)
  if(motorSpeedA < 10){motorSpeedA = 0;}
  if(motorSpeedB < 10){motorSpeedB = 0;}
  //Serial.println(motorSpeedA);
  //Serial.println(motorSpeedB);
  analogWrite(PA, motorSpeedA); // Send PWM signal to motor A
  analogWrite(PB, motorSpeedB); // Send PWM signal to motor B
}
  
void forword(){
  Serial.println("FOR");
  digitalWrite(DA, LOW);
  digitalWrite(DB, HIGH);
}

void backword(){    
  Serial.println("DOWN");
  digitalWrite(DA, HIGH);
  digitalWrite(DB, LOW);
}

void turnRight(){
  Serial.println("RIGHT");
  digitalWrite(DA, LOW);
  digitalWrite(DB, LOW);
}

void turnLeft(){
  Serial.println("LEFT");
  digitalWrite(DA, HIGH);
  digitalWrite(DB, HIGH);
}

void Stop(){
  Serial.println("STOP");
  motorSpeedA = 0;
  motorSpeedB = 0;
}
     
