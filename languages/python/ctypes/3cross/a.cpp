#include "cross.hpp"

extern "C" {
  void* createClass(){
    C* c=new C;
    c->name="world";
    return c;
  }
}
