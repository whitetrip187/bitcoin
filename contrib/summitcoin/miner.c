#include <openssl/sha.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
// usage: miner <header76hex> <bits hex> <start> <step>
static int hx(char c){return c<='9'?c-'0':(c|32)-'a'+10;}
int main(int ac,char**av){unsigned char h[80];for(int i=0;i<76;i++)h[i]=hx(av[1][2*i])*16+hx(av[1][2*i+1]);
 uint32_t bits=strtoul(av[2],0,16);unsigned char tgt[32]={0};int e=bits>>24;uint32_t m=bits&0xffffff;
 // target big-endian
 for(int i=0;i<3;i++){int pos=32-e+i; if(pos>=0&&pos<32) tgt[pos]=(m>>(8*(2-i)))&0xff;}
 uint64_t st=strtoull(av[3],0,10),sp=strtoull(av[4],0,10);
 for(uint64_t n=st;n<=0xffffffffULL;n+=sp){uint32_t nn=n;memcpy(h+76,&nn,4);unsigned char a[32],b[32];SHA256(h,80,a);SHA256(a,32,b);
  if(b[31]!=0 && e<=0x1f && tgt[0]==0) {} // quick reject below
  int ok=1;for(int i=0;i<32;i++){unsigned char x=b[31-i];if(x<tgt[i])break;if(x>tgt[i]){ok=0;break;}}
  if(ok){printf("%u ",nn);for(int i=31;i>=0;i--)printf("%02x",b[i]);printf("\n");return 0;}}
 printf("NONE\n");return 1;}
