#include <iomanip>
#include <ctime>
#include <string>
#include <sstream>

std::string timestamp(bool file=false){
    auto t=std::time(nullptr);
    std::stringstream ss;
    const char* format="%Y-%m-%d %H:%M:%S";
    if(file) format="%Y-%m-%d_%H-%M-%S";
    ss<<std::put_time(std::localtime(&t), format);
    return ss.str();
}

