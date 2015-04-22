/*
  rftester.cpp
  by Sarrailh Remi

  Description : This program test your RF receiver
*/

#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>


  RCSwitch mySwitch;

  int main(int argc, char *argv[]) {

   int pin;
   int received_code;
   int ok_code = 0;


   if(argc == 2) //Verify if there is an argument
   {
      pin = atoi(argv[1]); //Convert first argument to INT
      printf("PIN SELECTED :%i\n",pin);
    }
  else
  {
    printf("No PIN Selected\n");
    exit(1);
  }


/* IS WIRING PI INSTALLED ? */

    if(wiringPiSetup() == -1) //Initialize WiringPI
    {
      printf("WIRING PI NOT INSTALLED");
      exit(1);
    }

/* IS PIN RECEIVING RAW DATA */

    printf("---------------------\n");
    printf("TEST 1 - Received RAW digital\n");
    printf("--------------------\n");

    //We received GPIO State to see if something is happening
    for (int timer = 0; timer < 50; ++timer)
    {
      received_code = digitalRead(pin);
      if (received_code == 1) { ok_code++; } //If PIN IS HIGH add to ok_code
      printf("%i",digitalRead(pin));
      delay(10);
    }
    printf("\n");
    printf("--------------------\n");
    
    if (ok_code == 0) //If the PIN was never on HIGH we assume there was a problem
    {
      printf("TEST 1: FAIL\n");
      printf("Verify:\n");
      printf("1 - That you RF Receiver is correctly powered (VCC to 5V and GROUND to GND)\n");
      printf("2 - That you plugged DATA on the right pin\n");
      printf("////////////////////////////////////////////////////////\n");
      printf("RPI GPIO WIRING PI SCHEMATIC\n");
      printf("////////////////////////////////////////////////////////\n");
      printf("_____________________________________________________\n");
      printf("5V  5V  GND 15  16  1   GND 4   5   GND 6   10  11   \n");
      printf("o   o   o   o   o   o   o   o   o   o   o   o   o    \n");
      printf("o   o   o   o   o   o   o   o   o   o   o   o   o    \n");
      printf("3V  8   9   7   GND 0   2   3   3V  12  13  14  GND  \n");
      printf("_____________________________________________________\n");
      printf("P1\n");
      printf("////////////////////////////////////////////////////////\n");
      printf("DEFAULT WIRING\n");
      printf("////////////////////////////////////////////////////////\n");
      printf("_____________________________________________________\n");
      printf("5V      GND \n");
      printf("+   x   -   x   x   x   x   x   x   x   x   x   x    \n");
      printf("x   x   x   x   x   D   x   x   x   x   x   x   x    \n");
      printf("                    0 \n");
      printf("_____________________________________________________\n");
      printf("P1\n");
      exit(1);
    }
    else //If test1 PASS
{      

    printf("TEST 1: PASS\n");
    printf("\n");
    printf("---------------------\n");
    printf("TEST 2 - Receive Data\n");
    printf("---  INSTRUCTIONS ---\n");
    printf("Take a RCSwitch compatible remote\n");
    printf("And press any button\n");
    printf("A list of compatible devices is available here\n");
    printf("https://code.google.com/p/rc-switch/wiki/List_KnownDevices\n");
    printf("--------------------\n");

/* IS PIN RECEIVING RCSWITCH DATA */
   mySwitch = RCSwitch(); //Settings RCSwitch
   mySwitch.enableReceive(pin);


   while(1) { //Waiting for Data

    if (mySwitch.available()) { //If Data is present

      int value = mySwitch.getReceivedValue(); //Save Data in value
      printf("Code Received %i\n", mySwitch.getReceivedValue() ); //Show Code in Decimal
      break;   
    }

  }
  printf("--------------------\n");
  printf("TEST 2: PASS\n");
  printf("---------------------\n");
  printf("RF RECEIVER WAS SUCCESFULLY TESTED!\n");
  printf("\n");


  exit(0);
}
}
