#include <atomic>
#include <thread>

class Server{
	public:
		Server();
		~Server();
	private:
		std::atomic<bool> _quit;
		std::thread _thread;
		void* _server;
};
