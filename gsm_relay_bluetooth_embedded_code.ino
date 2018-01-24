#include <SoftwareSerial.h>
char dataString[50] = {0};
String data;
int led=13;
int a =0; 
#define RELAY1  7  
String number,message;
String str,str2;
SoftwareSerial mySerial(2, 3); // RX, TX
void setup() {
Serial.begin(9600);    
mySerial.begin(9600);
pinMode(RELAY1, OUTPUT);
digitalWrite(RELAY1,1);
}
  
void loop() {

    data=Serial.readString();
    if(data=="msg")
    {
       while(!Serial.available());
      number=Serial.readString();
      Serial.println("Sending Message....to "+number);
       while(!Serial.available());
      message=Serial.readString();
      mySerial.println("AT+CMGF=1");    //Sets the GSM Module in Text Mode
      delay(500);  // Delay of 1000 milli seconds or 1 second
      str2="AT+CMGS=\"+91"+number+"\"\r";
      mySerial.println(str2); // Replace x with mobile number
      delay(500);
      mySerial.println(message);// The SMS text you want to send
      delay(100);
      mySerial.println((char)26);// ASCII code of CTRL+Z
      Serial.println("MESSAGE SENT");
      delay(1000);
    }
     if(data=="Call")
    {
      delay(100);
      while(!Serial.available());
      number=Serial.readString();
      digitalWrite(led,HIGH);
      Serial.print("number is :"+number);
      str="ATD"+number+";";
       //Serial.print(str);
      mySerial.println(str); // ATDxxxxxxxxxx; -- watch out here for semicolon at the end!!
      Serial.print("CALLING NUMBER "+number+"  WAit");
      delay(2000);
      //Serial.print(number);// give the loop some break
     // digitalWrite(RELAY1,0); 
    }
    if(data=="Lights on")
    {
      digitalWrite(led,HIGH);
      Serial.write("Correct\n");// give the loop some break
      digitalWrite(RELAY1,0); 
    }
    if(data=="Lights off")
    {
      digitalWrite(led,LOW);
      Serial.write("Correct\n");// give the loop some break
      digitalWrite(RELAY1,1); 
    }
    data="";
      delay(200);
  //}
}
