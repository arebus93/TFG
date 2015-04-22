 /*
  rfreceive.cpp
  by Sarrailh Remi
  Description : This code receives RF codes and trigger actions
*/

#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>

  RCSwitch mySwitch;
  int pin; //Pin of the RF receiver
  int codereceived; // Code received
  int bitreceived; // Nbits received  
  float Temp=0;
  float Pres=0;
  int Hum=0;
  int Luz=0;

  int main(int argc, char *argv[]) {
	  
	if(argc == 2) { //Verify if there is an argument
      pin = atoi(argv[1]); //Convert first argument to INT
      printf("PIN SELECTED :%i\n",pin);
    }
  else {
    printf("No PIN Selected\n");
    printf("Usage: rfreceive PIN\n");
    printf("Example: rfreceive 0\n");
    exit(1);
  }

    if(wiringPiSetup() == -1) { //Initialize WiringPI
      printf("Wiring PI is not installed\n"); //If WiringPI is not installed give indications
      printf("You can install it with theses command:\n");
      printf("apt-get install git-core\n");
      printf("git clone git://git.drogon.net/wiringPi\n");
      printf("cd wiringPi\n"); 
      printf("git pull origin\n");
      printf("./build\n");
      exit(1);
    }

   mySwitch = RCSwitch(); //Settings RCSwitch (with first argument as pin)
   mySwitch.enableReceive(pin);

   while(1) { //Infinite loop
    if (mySwitch.available()) { 
        if( mySwitch.getReceivedValue()){ ; //Starting frame
	  	codereceived = mySwitch.getReceivedValue(); //Get data in decimal
		bitreceived = mySwitch.getReceivedBitlength();

		switch(bitreceived){
                	case 7: Hum=codereceived; break;
	 		case 9: Luz=codereceived; break;
			case 16:Temp=(codereceived/100.00);break;
			case 18:Pres=(codereceived/100.00);break; 
	       		default:break;
		}
	     mySwitch.resetAvailable();
		if((Temp!=0) && (Hum != 0) && (Pres != 0) && (Luz !=0)){
		printf("\n");
  		printf("Temp: %f Hum: %d Luz: %d Pres: %f\n", Temp,Hum,Luz,Pres);
	  	Temp=Hum=Pres=Luz=0;
		} 
	  }
          //Want to execute something when a code is received ?
          //When 12345 is received this will execute program_to_execute for exemple)
          /*
          if (codereceived == 12345)
          {
            system("program_to_execute");
          }
          */
    }
  mySwitch.resetAvailable();
  }
}
