// Disposable diagnostic preload, never linked into Ox. Logs >=16KiB allocations
// and all frees for offline live-allocation reconstruction. Not an RSS acceptance run.
#define _GNU_SOURCE
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <execinfo.h>
#include <stdio.h>
#include <stdint.h>
extern void *__libc_malloc(size_t);
extern void *__libc_calloc(size_t,size_t);
extern void *__libc_realloc(void*,size_t);
extern void __libc_free(void*);
static __thread int busy;
static int fd=-1;
static void logop(char op,void *p,size_t size) {
 if(busy||fd<0)return;
 busy=1;
 char row[512];void *bt[12];int n=0;
 if(op=='A')n=backtrace(bt,12);
 int len=snprintf(row,sizeof row,"%c %p %zu",op,p,size);
 for(int i=2;i<n;i++)len+=snprintf(row+len,sizeof(row)-len," %p",bt[i]);
 row[len++]='\n';write(fd,row,len);busy=0;
}
__attribute__((constructor))static void init(void){busy=1;fd=open(getenv("OX_ALLOC_LOG"),O_WRONLY|O_CREAT|O_EXCL,0600);busy=0;}
void *malloc(size_t s){void*p=__libc_malloc(s);if(s>=16384)logop('A',p,s);return p;}
void *calloc(size_t n,size_t s){void*p=__libc_calloc(n,s);if(n*s>=16384)logop('A',p,n*s);return p;}
void free(void*p){if(p)logop('F',p,0);__libc_free(p);}
void *realloc(void*p,size_t s){void*q=__libc_realloc(p,s);if(q||!s)logop('F',p,0);if(q&&s>=16384)logop('A',q,s);return q;}
