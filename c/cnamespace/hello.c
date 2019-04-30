//main file
#include <stdio.h>

#include "namespace.h"

void NAMESPACED(hello)(){
	printf("Hello, world!\n");
}

int main(){
	LOL_hello();
	return 0;
}
