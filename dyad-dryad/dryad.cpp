#include "dryad.hpp"

#include <dyad.h>

#include <atomic>
#include <map>
#include <mutex>
#include <thread>

#include <iostream>
#include <sstream>

namespace DRYAD_NAMESPACE{

class Mutex{
	public:
		void lock(){
			std::stringstream ss;
			ss<<std::this_thread::get_id();
			std::string s=ss.str();
			printf("%s locking %p\n", s.c_str(), this);
			_mutex.lock();
			printf("%s locked %p\n", s.c_str(), this);
		}
		void unlock(){
			std::stringstream ss;
			ss<<std::this_thread::get_id();
			printf("%s unlocking %p\n", ss.str().c_str(), this);
			_mutex.unlock();
		}
	private:
		std::recursive_mutex _mutex;
};

static void onAccept(dyad_Event* e);
static void onData(dyad_Event* e);

class Boss{
	public:
		Boss(){
			printf("dryad boss %p %s\n", this, DRYAD_PREFIX);
			dyad_init();
			dyad_setUpdateTimeout(1);
			_quit=false;
			_thread=std::thread([this](){
				std::stringstream ss;
				ss<<std::this_thread::get_id();
				printf("dyad_update thread %s\n", ss.str().c_str());
				while(!_quit){
					_mutex.lock();
					dyad_update();
					_mutex.unlock();
				}
			});
			printf("dryad boss constructor returning\n");
		}
		~Boss(){
			_quit=true;
			_thread.join();
		}
		dyad_Stream* server(std::string host, int port, Receiver receiver){
			printf("dryad boss %p server 1\n", this);
			_mutex.lock();
			printf("dryad boss %p server 2\n", this);
			auto stream=dyad_newStream();
			printf("dryad boss %p server 3\n", this);
			_receivers[stream]=receiver;
			dyad_addListener(stream, DYAD_EVENT_ACCEPT, onAccept, NULL);
			dyad_listenEx(stream, host.c_str(), port, 511);
			printf("dryad boss %p server 4\n", this);
			_mutex.unlock();
			printf("dryad boss %p server 5\n", this);
			return stream;
		}
		dyad_Stream* client(std::string host, int port, Receiver receiver){
			printf("dryad boss %p client locking mutex\n", this);
			_mutex.lock();
			printf("dryad boss %p client locked mutex\n", this);
			auto stream=dyad_newStream();
			_receivers[stream]=receiver;
			dyad_addListener(stream, DYAD_EVENT_DATA, onData, NULL);
			dyad_connect(stream, host.c_str(), port);
			_mutex.unlock();
			return stream;
		}
		void accept(dyad_Event* e){
			_mutex.lock();
			_accepted[e->stream].push_back(e->remote);
			_receivers[e->remote]=_receivers[e->stream];
			dyad_addListener(e->remote, DYAD_EVENT_DATA, onData, NULL);
			_mutex.unlock();
		}
		void broadcast(dyad_Stream* stream, const std::vector<uint8_t>& data){
			_mutex.lock();
			for(auto i: _accepted[stream]) dyad_write(i, data.data(), data.size());
			_mutex.unlock();
		}
		void send(dyad_Stream* stream, const std::vector<uint8_t>& data){
			_mutex.lock();
			dyad_write(stream, data.data(), data.size());
			_mutex.unlock();
		}
		void receive(dyad_Event* e){
			_mutex.lock();
			auto receiver=_receivers[e->stream];
			_mutex.unlock();
			receiver(std::vector<uint8_t>(e->data, e->data+e->size));
		}
		void close(dyad_Stream* stream){
			_mutex.lock();
			dyad_removeAllListeners(stream, DYAD_EVENT_NULL);
			if(_accepted.count(stream)){
				for(auto i: _accepted[stream]){
					dyad_removeAllListeners(i, DYAD_EVENT_NULL);
					_receivers.erase(i);
				}
			}
			_receivers.erase(stream);
			_accepted.erase(stream);
			_mutex.unlock();
		}
	private:
		std::atomic<bool> _quit;
		std::thread _thread;
		Mutex _mutex;
		std::map<dyad_Stream*, Receiver> _receivers;
		std::map<dyad_Stream*, std::vector<dyad_Stream*>> _accepted;
};

static Boss* fBoss;

static void onAccept(dyad_Event* e){ fBoss->accept(e); }
static void onData(dyad_Event* e){ fBoss->receive(e); }

void start(){
	fBoss=new Boss;
	printf("dryad boss pointer %p %p %s\n", &fBoss, fBoss, DRYAD_PREFIX);
}
void finish(){ delete fBoss; }

Server::Server(std::string host, int port, Receiver receiver){
	_stream=fBoss->server(host, port, receiver);
}

Server::~Server(){ fBoss->close((dyad_Stream*)_stream); }

void Server::send(const std::vector<uint8_t>& data){
	fBoss->broadcast((dyad_Stream*)_stream, data);
}

Client::Client(std::string host, int port, Receiver receiver){
	_stream=fBoss->client(host, port, receiver);
}

Client::~Client(){ fBoss->close((dyad_Stream*)_stream); }

void Client::send(const std::vector<uint8_t>& data){
	fBoss->send((dyad_Stream*)_stream, data);
}

}//namespace
