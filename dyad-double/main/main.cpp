#include <server.hpp>
#include <client.hpp>

#include <iostream>
#include <string>
#include <thread>
#include <sstream>

int main(){
	{
		std::stringstream ss;
		ss<<std::this_thread::get_id();
		printf("main started, thread: %s\n", ss.str().c_str());
		Server server;
		printf("main server constructed\n");
		Client client;
		printf("main client constructed\n");
		std::string s;
		std::cin>>s;
	}
}
