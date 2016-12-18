/*
 Usage: see printUsage()
 */

#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <iostream>

void printUsage()
{
	std::cout << "  Usage: sudo ./send433 <groupCode> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send433 01011 3 1\n";
	std::cout << "         sudo ./send433 <groupNumber> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send433 4 3 0\n";
	std::cout << "         sudo ./send433 <familyCharacter> <groupNumber> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send433 c 2 3 1\n";
	std::cout << "         sudo ./send433 <dipSwitchGroup> <dipSwitchUnit> <command>\n";
	std::cout << "    e.g. sudo ./send433 11100 00001 1\n";
	std::cout << "         sudo ./send433 <id> <all> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send433 123456 0 1 0\n";
	std::cout << "\n";
	std::cout << "  Command is 0 for OFF and 1 for ON.\n";
	std::cout << "  All is 0 for single switch and 1 for all switches in group.\n";
	std::cout << "\n";
	std::cout << "  You can use -p=PIN to set the GPIO pin and -pl=PULSELENGTH to set the pulse length. If you use both options,\n";
	std::cout << "  please use them in this order: sudo ./send433 -p=PIN -pl=PULSELENGTH <OTHEROPTIONS>\n\n";
}

int main(int argc, char *argv[]) {
    
    /*
     see https://projects.drogon.net/raspberry-pi/wiringpi/pins/
     for pin mapping of the raspberry pi GPIO connector
     */
    int PIN = 0;
    int overridePIN = 0;
    int PULSELENGTH = 0;
	if(argc > 4) {
		std::string arg = argv[1];
		if( arg.substr(0,3) == "-p=" ) {
			overridePIN ++;
			if(atoi(arg.substr(3).c_str()) > 0) {
				PIN = atoi(arg.substr(3).c_str());
				printf("Setting PIN to %i\n", PIN);
			}
		}
		arg = argv[1];
		if( arg.substr(0,4) == "-pl=" ) {
			overridePIN ++;
			if(atoi(arg.substr(4).c_str()) > 0) {
				PULSELENGTH = atoi(arg.substr(4).c_str());
				printf("Setting PulseLength to %i\n", PULSELENGTH);
			}
		} else {
			arg = argv[2];
			if( arg.substr(0,4) == "-pl=" ) {
				overridePIN ++;
				if(atoi(arg.substr(4).c_str()) > 0) {
					PULSELENGTH = atoi(arg.substr(4).c_str());
					printf("Setting PulseLength to %i\n", PULSELENGTH);
				}
			}
		}
	}
	if (wiringPiSetup () == -1) return 1;
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN);
	if (PULSELENGTH > 0) {
		mySwitch.setPulseLength(PULSELENGTH);
	}
	
	if(argc == 4+overridePIN)
	{
		char* sGroup = argv[1+overridePIN];
		char* sSwitch = argv[2+overridePIN];
		int nSwitchNumber = atoi(argv[2+overridePIN]);

		int command  = atoi(argv[3+overridePIN]);
		
		if(strlen(sGroup) > 2)
		{
			//Type A: 10 pole DIP switches
			printf("sending [Type A] groupCode[%s] switchNumber[%s] command[%i]\n", sGroup, sSwitch, command);
			switch(command) {
				case 1:
					if (strlen(sSwitch) > 2) {
						mySwitch.switchOn(sGroup, sSwitch);
					} else {
						mySwitch.switchOn(sGroup, nSwitchNumber);
					}
					break;
				case 0:
					if (strlen(sSwitch) > 2) {
						mySwitch.switchOff(sGroup, sSwitch);
					} else {
						mySwitch.switchOff(sGroup, nSwitchNumber);
					}
					break;
				default:
					printf("command[%i] is unsupported\n", command);
					printUsage();
					return -1;
			}
			return 0;
		} else {
			//Type B: Two rotary/sliding switches
			int nGroupNumber = atoi(sGroup);
			printf("sending [Type B] groupNumber[%i] switchNumber[%i] command[%i]\n", nGroupNumber, nSwitchNumber, command);
			switch(command) {
				case 1:
					mySwitch.switchOn(nGroupNumber, nSwitchNumber);
					break;
				case 0:
					mySwitch.switchOff(nGroupNumber, nSwitchNumber);
					break;
				default:
					printf("command[%i] is unsupported\n", command);
					printUsage();
					return -1;
			}
			return 0;
		}
	}
	else if(argc == 5+overridePIN)
	{
	    //Type C: Intertechno V1 and Type D: Intertechno V2
		char* sFamily = argv[1+overridePIN];
		int nGroup = atoi(argv[2+overridePIN]);
		int nDevice = atoi(argv[3+overridePIN]);
		int command = atoi(argv[4+overridePIN]);
		if (strlen(sFamily) > 1) {
			mySwitch.setProtocol(3);
			mySwitch.setRepeatTransmit(10);
			long lid = atol(sFamily);
			printf("sending [Type D] id[%i] all[%i] unit[%i] command[%i]\n", lid, nGroup, nDevice, command);
			switch(command) {
				case 1:
					mySwitch.switchOn(lid,nGroup,nDevice);
					break;
				case 0:
					mySwitch.switchOff(lid,nGroup,nDevice);
					break;
				default:
					printf("command[%i] is unsupported\n", command);
					printUsage();
					return -1;
			}
			return 0;
		} else {
    			printf("sending [Type C] family[%s] groupNumber[%i] switchNumber[%i] command[%i]\n", sFamily, nGroup, nDevice, command);
			switch(command) {
				case 1:
					mySwitch.switchOn(sFamily[0], nGroup, nDevice);
					break;
				case 0:
					mySwitch.switchOff(sFamily[0], nGroup, nDevice);
					break;
				default:
					printf("command[%i] is unsupported\n", command);
					printUsage();
					return -1;
			}
			return 0;
		}
	}
	else
	{
		printUsage();
	}
	return 1;
}
