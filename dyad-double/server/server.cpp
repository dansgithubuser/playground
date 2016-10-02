#include "server.hpp"

#include <dryad.hpp>

#include <iostream>
#include <thread>
#include <sstream>

static void receiver(const std::vector<uint8_t>& data){
	std::cout<<"server rx: ";
	for(auto i: data) std::cout<<i<<" ";
	std::cout<<"\n";
}

Server::Server(){
	printf("Server::Server 1\n");
	dryad_server::start();
	printf("Server::Server 2\n");
	_server=new dryad_server::Server("127.0.0.1", 9089, receiver);
	printf("Server::Server 3\n");
	_quit=false;
	_thread=std::thread([this](){
		std::stringstream ss;
		ss<<std::this_thread::get_id();
		printf("server thread %s\n", ss.str().c_str());
		while(!_quit){
			std::this_thread::sleep_for(std::chrono::seconds(1));
			printf("server sending\n");
			((dryad_server::Server*)_server)->send({'j', 'k', 'l', ';'});
		}
		printf("server thread done\n");
	});
	printf("Server::Server 4\n");
}

Server::~Server(){
	_quit=true;
	printf("server quitting\n");
	_thread.join();
	printf("server joined\n");
	delete _server;
	printf("server deleted\n");
	dryad_server::finish();
	printf("server finished\n");
}
