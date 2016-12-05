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
	std::cout << "  Usage: sudo ./send <groupCode> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send 01011 3 1\n";
	std::cout << "         sudo ./send <groupNumber> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send 4 3 0\n";
	std::cout << "         sudo ./send <familyCharacter> <groupNumber> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send c 2 3 1\n";
	std::cout << "         sudo ./send <dipSwitchGroup> <dipSwitchUnit> <command>\n";
	std::cout << "    e.g. sudo ./send 11100 00001 1\n";
	std::cout << "         sudo ./send <id> <all> <switchNumber> <command>\n";
	std::cout << "    e.g. sudo ./send 123456 0 1 0\n";
	std::cout << "\n";
	std::cout << "  Command is 0 for OFF and 1 for ON\n";
	std::cout << "  All is 0 for single Switch and 1 for all Switches in Group\n";
	std::cout << "\n";
	std::cout << "  See http://code.google.com/p/rc-switch/wiki/HowTo_OperateLowCostOutlets for more information about supported switches\n";
}

int main(int argc, char *argv[]) {
    
    /*
     output PIN is hardcoded for testing purposes
     see https://projects.drogon.net/raspberry-pi/wiringpi/pins/
     for pin mapping of the raspberry pi GPIO connector
     */
    int PIN = 0;
    int overridePIN = 0;
	if(argc > 4) {
		std::string arg = argv[1];
		if( arg.substr(0,3) == "-p=" ) {
			overridePIN = 1;
			if(atoi(arg.substr(3).c_str()) > 0) {
				PIN = atoi(arg.substr(3).c_str());
			}
		}
	}
	if (wiringPiSetup () == -1) return 1;
	RCSwitch mySwitch = RCSwitch();
	mySwitch.enableTransmit(PIN);
	
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
	    //Type C: Intertechno
		char* sFamily = argv[1+overridePIN];
		int nGroup = atoi(argv[2+overridePIN]);
		int nDevice = atoi(argv[3+overridePIN]);
		int command = atoi(argv[4+overridePIN]);
		if (strlen(sFamily) > 1) {
			mySwitch.setProtocol(3);
			mySwitch.setRepeatTransmit(10);
			long lid = atol(sFamily);
			printf("sending arctech_switch id[%i] all[%i] unit[%i] command[%i]\n", lid, nGroup, nDevice, command);
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
