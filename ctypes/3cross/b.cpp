#include "cross.hpp"

extern "C" {
  void consumeClass(void* c){ ((C*)c)->hello(); }
}
