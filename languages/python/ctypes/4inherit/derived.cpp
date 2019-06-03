#include "base.hpp"

class Derived: public Base{
  public:
    virtual void hello(){ std::cout<<"Hello world!\n"; }
};

extern "C" {
  void* create(){ return (Base*)new Derived; }
}
