#include <stdio.h>

int main(){
	freopen("stderr.txt", "w", stderr);
	fprintf(stderr, "hello?\n");
	return 0;
}
