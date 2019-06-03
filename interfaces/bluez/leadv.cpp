#include "common.hpp"

#include "../timestamp.h"

#include <cstdlib>
#include <iostream>

std::vector<uint8_t> advert={0x07, 0xff, 0xde, 0xde, 0x1b, 0xad, 0xba, 0xbe};

int main(){
	std::cout<<"finding device\n";
	auto deviceId=bluez::find();
	std::cout<<"opening device\n";
	auto deviceDescriptor=bluez::open(deviceId);
	std::cout<<"disabling advert\n";
	bluez::toggleAdvert(deviceDescriptor, false);
	std::cout<<"setting advert\n";
	bluez::setAdvert(deviceDescriptor, advert);
	std::cout<<"enabling advert\n";
	bluez::toggleAdvert(deviceDescriptor, true);
	std::cout<<"enter q to quit\n";
	std::string s;
	std::cin>>s;
	bluez::close(deviceDescriptor);
	return 0;
}

