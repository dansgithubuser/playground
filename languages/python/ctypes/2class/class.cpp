#include <iostream>

class C{
  public:
    void hello(){ std::cout<<"Hello!\n"; }
};

extern "C" {
  void* createClass(){ return new C; }
  void consumeClass(void* c){ ((C*)c)->hello(); }
}
