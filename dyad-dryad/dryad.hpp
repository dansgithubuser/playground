#ifndef DRYAD_HPP_INCLUDED
#define DRYAD_HPP_INCLUDED

#include <cstdint>
#include <functional>
#include <string>
#include <vector>

namespace dryad{
	void start();//must be called after static initialization
	void finish();//must be called before static destruction
	typedef std::function<void(const std::vector<uint8_t>&)> Receiver;
	class Server{
		public:
			Server(std::string host, int port, Receiver);
			~Server();//must be called before finish
			void send(const std::vector<uint8_t>&);
		private:
			void* _stream;
	};
	class Client{
		public:
			Client(std::string host, int port, Receiver);
			~Client();//must be called before finish
			void send(const std::vector<uint8_t>&);
		private:
			void* _stream;
	};
}

#endif
