#include "base.hpp"

extern "C" {
  void* create(){ return new Base; }
  void consume(void* c){ ((Base*)c)->hello(); }
}
