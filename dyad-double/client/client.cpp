#include "client.hpp"

#include <dryad.hpp>

#include <iostream>
#include <thread>
#include <sstream>

static void receiver(const std::vector<uint8_t>& data){
	std::cout<<"client rx: ";
	for(auto i: data) std::cout<<i<<" ";
	std::cout<<"\n";
}

Client::Client(){
	printf("Client::Client 1\n");
	dryad_client::start();
	printf("Client::Client 2\n");
	_client=new dryad_client::Client("127.0.0.1", 9089, receiver);
	printf("Client::Client 3\n");
	_quit=false;
	_thread=std::thread([this](){
		std::stringstream ss;
		ss<<std::this_thread::get_id();
		printf("client thread %s\n", ss.str().c_str());
		while(!_quit){
			std::this_thread::sleep_for(std::chrono::seconds(1));
			printf("client sending\n");
			((dryad_client::Client*)_client)->send({'a', 's', 'd', 'f'});
		}
		printf("client thread done\n");
	});
	printf("Client::Client 10\n");
}

Client::~Client(){
	_quit=true;
	printf("client quitting\n");
	_thread.join();
	printf("client joined\n");
	delete _client;
	printf("client deleted\n");
	dryad_client::finish();
	printf("client finished\n");
}
