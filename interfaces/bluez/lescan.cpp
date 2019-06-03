#include "common.hpp"

#include "../timestamp.h"

#include <iostream>
#include <thread>

int main(){
	std::cout<<"finding device\n";
	auto deviceId=bluez::find();
	std::cout<<"opening device\n";
	auto deviceDescriptor=bluez::open(deviceId);
	std::cout<<"setting scan parameters\n";
	bluez::setScanParameters(deviceDescriptor, 0x12, 0x12);
	std::cout<<"starting scan\n";
	bluez::toggleScan(deviceDescriptor, true);
	std::cout<<"starting inquiry thread, enter q to quit\n";
	bool quit=false;
	std::thread thread([&quit, deviceDescriptor](){
		while(!quit){
			std::cout
				<<timestamp()
				<<" making inquiry... "
				<<bluez::toString(bluez::inquire(deviceDescriptor))
				<<" ...inquiry complete\n"
			;
		}
	});
	std::string s;
	std::cin>>s;
	quit=true;
	thread.join();
	bluez::close(deviceDescriptor);
	return 0;
}

