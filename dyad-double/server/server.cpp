#include "server.hpp"

#include <dryad.hpp>

#include <iostream>

static void receiver(const std::vector<uint8_t>& data){
	std::cout<<"server rx: ";
	for(auto i: data) std::cout<<i<<" ";
	std::cout<<"\n";
}

Server::Server(){
	dryad::start();
	_server=new dryad::Server("127.0.0.1", 9089, receiver);
	_quit=false;
	_thread=std::thread([this](){
		while(!_quit){
			std::this_thread::sleep_for(std::chrono::seconds(1));
			((dryad::Server*)_server)->send({'j', 'k', 'l', ';'});
		}
	});
}

Server::~Server(){
	_quit=true;
	_thread.join();
	delete _server;
	dryad::finish();
}
