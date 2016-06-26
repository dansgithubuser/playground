#include <cstdint>
#include <iomanip>
#include <sstream>
#include <string>

std::string hex(uint8_t x){
	std::stringstream ss;
	ss<<std::hex<<std::setw(2)<<std::setfill('0')<<(unsigned)x;
	return ss.str();
}

std::string hex(uint8_t* x, unsigned size){
	std::stringstream ss;
	for(unsigned i=0; i<size; ++i) ss<<hex(x[i])<<" ";
	return ss.str();
}

#include <iostream>

int main(){
	uint8_t x[]={63, 23, 115, 74, 34, 1, 7, 229};
	std::cout<<hex(x, sizeof(x));
	return 0;
}
