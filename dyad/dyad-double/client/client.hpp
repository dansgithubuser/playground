#include <atomic>
#include <thread>

class Client{
	public:
		Client();
		~Client();
	private:
		std::atomic<bool> _quit;
		std::thread _thread;
		void* _client;
};
