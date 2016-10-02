#include "client.hpp"

#include <dryad.hpp>

#include <iostream>

static void receiver(const std::vector<uint8_t>& data){
	std::cout<<"client rx: ";
	for(auto i: data) std::cout<<i<<" ";
	std::cout<<"\n";
}

Client::Client(){
	dryad_client::start();
	_client=new dryad_client::Client("127.0.0.1", 9089, receiver);
	_quit=false;
	_thread=std::thread([this](){
		while(!_quit){
			std::this_thread::sleep_for(std::chrono::seconds(1));
			((dryad_client::Client*)_client)->send({'a', 's', 'd', 'f'});
		}
	});
}

Client::~Client(){
	_quit=true;
	_thread.join();
	delete _client;
	dryad_client::finish();
}
