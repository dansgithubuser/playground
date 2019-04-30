#include "dyad.h"

#include <stdio.h>

static void addListeners(dyad_Stream*);

static void atPanic(const char* message){ printf("panic: %s\n", message); }

static dyad_Stream* fStreams[256];
static unsigned fStreamsI=0;

static void atEvent(dyad_Event* event){
	int i;
	const char* types[]={
		"NULL",
		"DESTROY",
		"ACCEPT",
		"LISTEN",
		"CONNECT",
		"CLOSE",
		"READY",
		"DATA",
		"LINE",
		"ERROR",
		"TIMEOUT",
		"TICK"
	};
	if(event->type==DYAD_EVENT_TICK) return;
	printf("event: %d %s\n", event->type, types[event->type]);
	printf("\tstream: %p\n", event->stream);
	printf("\tremote: %p\n", event->remote);
	printf("\tmsg   : %s\n", event->msg);
	printf("\tdata  : ");
	for(i=0; i<event->size; ++i) printf("%.2x ", event->data[i]);
	printf("\n");
	if(event->remote){
		printf("saving remote as stream %d\n", fStreamsI);
		addListeners(event->remote);
		fStreams[fStreamsI++]=event->remote;
	}
}

static void addListeners(dyad_Stream* stream){
	unsigned i;
	for(i=DYAD_EVENT_NULL; i<=DYAD_EVENT_TICK; ++i)
		dyad_addListener(stream, i, atEvent, NULL);
}

int main(){
	dyad_atPanic(atPanic);
	dyad_init();
	while(1){
		char c;
		scanf("%c", &c);
		if(c=='q') break;
		else if(c=='s'){
			dyad_Stream* stream;
			stream=dyad_newStream();
			printf("stream: %d %p\n", fStreamsI, stream);
			addListeners(stream);
			fStreams[fStreamsI++]=stream;
		}
		else if(c=='l'){
			int i;
			char ip[64];
			int port;
			scanf("%d %s %d", &i, ip, &port);
			printf("listen: %d\n", dyad_listenEx(fStreams[i], ip, port, 511));
		}
		else if(c=='c'){
			int i;
			char ip[64];
			int port;
			scanf("%d %s %d", &i, ip, &port);
			printf("connect: %d\n", dyad_connect(fStreams[i], ip, port));
		}
		else if(c=='w'){
			int i;
			unsigned j, data;
			scanf("%d %x", &i, &data);
			printf("writing ");
			for(j=0; j<sizeof(data); ++j) printf("%.2x ", ((char*)&data)[j]);
			printf("\n");
			dyad_write(fStreams[i], &data, sizeof(data));
		}
		else if(c=='u') dyad_update();
	}
	dyad_shutdown();
	return 0;
}
