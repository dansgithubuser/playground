#include <stdio.h>

/*
>gcc -v
Configured with: --prefix=/Applications/Xcode.app/Contents/Developer/usr --with-gxx-include-dir=/usr/include/c++/4.2.1
Apple LLVM version 6.0 (clang-600.0.57) (based on LLVM 3.5svn)
Target: x86_64-apple-darwin13.4.0
Thread model: posix
>gcc cpreprocessor.c -DD; ./a.out
D is 1
*/

int main(){
	#ifdef D
		#if D==0
			printf("D is 0\n");
		#elif D==1
			printf("D is 1\n");
		#elif D>0
			printf("D>0\n");
		#elif D<0
			printf("D<0\n");
		#endif
	#else
		printf("D is undefined\n");
	#endif
	return 0;
}

