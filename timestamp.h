#ifdef __cplusplus
extern "C" {
#endif

#include <time.h>

char _timestamp_buffer[32];

const char* timestamp(){
	time_t now=time(NULL);
	struct tm t=*localtime(&now);
	strftime(_timestamp_buffer, sizeof _timestamp_buffer, "%Y-%m-%d %H:%M:%S", &t);
	return _timestamp_buffer;

}

#ifdef __cplusplus
}
#endif
