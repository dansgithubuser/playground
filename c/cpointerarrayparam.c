#include <stdint.h>
#include <stdio.h>

typedef uint8_t Block[5];

//array parameters become pointers -- ie T x[N] becomes T* x
void f(Block x){
	printf("%lu %lu\n", sizeof(x), sizeof(x[0]));
}

//pointer-to-array parameters are not array parameters -- their types remain untouched like everything else
void g(Block* x){
	printf("%lu %lu\n", sizeof(*x), sizeof((*x)[0]));
}

int main(){
	Block x;
	f(x);
	g(&x);
	return 0;
}

