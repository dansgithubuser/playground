#include "dryad.hpp"

#include <dyad.h>

#include <atomic>
#include <map>
#include <mutex>
#include <thread>

namespace DRYAD_NAMESPACE{

static void onAccept(dyad_Event* e);
static void onData(dyad_Event* e);

class Boss{
	public:
		Boss(){
			dyad_init();
			dyad_setUpdateTimeout(1e-3);
			_quit=false;
			_thread=std::thread([this](){ while(!_quit){
				_mutex.lock();
				dyad_update();
				_mutex.unlock();
			} });
		}
		~Boss(){
			_quit=true;
			_thread.join();
		}
		dyad_Stream* server(std::string host, int port, Receiver receiver){
			_mutex.lock();
			auto stream=dyad_newStream();
			_receivers[stream]=receiver;
			dyad_addListener(stream, DYAD_EVENT_ACCEPT, onAccept, NULL);
			dyad_listenEx(stream, host.c_str(), port, 511);
			_mutex.unlock();
			return stream;
		}
		dyad_Stream* client(std::string host, int port, Receiver receiver){
			_mutex.lock();
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
		std::recursive_mutex _mutex;
		std::map<dyad_Stream*, Receiver> _receivers;
		std::map<dyad_Stream*, std::vector<dyad_Stream*>> _accepted;
};

static Boss* fBoss;

static void onAccept(dyad_Event* e){ fBoss->accept(e); }
static void onData(dyad_Event* e){ fBoss->receive(e); }

void start(){ fBoss=new Boss; }
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
