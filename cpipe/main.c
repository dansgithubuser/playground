#include <stdio.h>

int main(){
	printf("(w)rite or (r)ead? ");
	char s[4096];
	scanf("%c", s);
	FILE* f;
	if(s[0]=='w'){
		f=fopen("file.txt", "w");
		while(1){
			printf("write: ");
			scanf("%s", s);
			fprintf(f, "%s", s);
			fflush(f);
		}
	}
	else{
		f=fopen("file.txt", "a+");
		while(1){
			scanf("%c", s);
			int r=fscanf(f, "%s", s);
			if(r!=EOF) printf("read %d: %s\n", r, s);
			else printf("nothing new to read\n");
		}
	}
}
