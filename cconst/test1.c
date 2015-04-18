#include "declarations.h"

#include <stdio.h>

const char* guys_p="guys";

int main(){
	hello_p="Hey";
	world_pp=&guys_p;
	printf("%s, %s!\n", *hello_pp, *world_pp);
	return 0;
}

