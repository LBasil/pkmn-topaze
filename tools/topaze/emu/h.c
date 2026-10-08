#include <mgba/core/core.h>
#include <mgba-util/image.h>
#include <mgba/core/config.h>
#include <mgba/gba/core.h>
#include <mgba/core/config.h>
#include <mgba/internal/gba/input.h>
#include <mgba-util/vfs.h>
#include <mgba/core/serialize.h>
#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <string.h>
// usage: h rom script   ; script: run N | key NAME N | shot file.ppm | read ADDR LEN | save file | load file
static struct mCore *core; static mColor *buf; static unsigned W,H;
static void run(int n){for(int i=0;i<n;i++)core->runFrame(core);}
static int keyid(const char*s){ if(!strcmp(s,"A"))return GBA_KEY_A; if(!strcmp(s,"B"))return GBA_KEY_B; if(!strcmp(s,"START"))return GBA_KEY_START; if(!strcmp(s,"SELECT"))return GBA_KEY_SELECT; if(!strcmp(s,"UP"))return GBA_KEY_UP; if(!strcmp(s,"DOWN"))return GBA_KEY_DOWN; if(!strcmp(s,"LEFT"))return GBA_KEY_LEFT; if(!strcmp(s,"RIGHT"))return GBA_KEY_RIGHT; if(!strcmp(s,"L"))return GBA_KEY_L; if(!strcmp(s,"R"))return GBA_KEY_R; return -1;}
int main(int c,char**v){
 core=GBACoreCreate(); core->init(core); mCoreInitConfig(core,NULL);
 core->baseVideoSize(core,&W,&H); buf=malloc(W*H*4); core->setVideoBuffer(core,buf,W);
 struct VFile*vf=VFileOpen(v[1],O_RDONLY); if(!vf||!core->loadROM(core,vf)){puts("loadfail");return 1;}
 core->reset(core);
 FILE*f=fopen(v[2],"r"); char l[512];
 while(fgets(l,sizeof l,f)){ char a[64],b[256]; int n=0;
  if(sscanf(l,"run %d",&n)==1) run(n);
  else if(sscanf(l,"key %63s %d",a,&n)==2){ int k=keyid(a); core->setKeys(core,1<<k); run(n); core->setKeys(core,0); run(8);}
  else if(sscanf(l,"shot %255s",b)==1){ FILE*o=fopen(b,"wb"); fprintf(o,"P6\n%u %u\n255\n",W,H); for(unsigned i=0;i<W*H;i++){unsigned p=buf[i];fputc(p&0xff,o);fputc((p>>8)&0xff,o);fputc((p>>16)&0xff,o);} fclose(o);}
  else if(sscanf(l,"ss %255s",b)==1){ struct VFile*o=VFileOpen(b,O_CREAT|O_TRUNC|O_RDWR); mCoreSaveStateNamed(core,o,SAVESTATE_SAVEDATA|SAVESTATE_RTC); o->close(o);}
  else if(sscanf(l,"ls %255s",b)==1){ struct VFile*o=VFileOpen(b,O_RDONLY); if(o){ mCoreLoadStateNamed(core,o,SAVESTATE_SAVEDATA|SAVESTATE_RTC); o->close(o);} else puts("R: nostate");}
  else if(sscanf(l,"readp %63s %63s %d",a,b,&n)==3){ unsigned p=core->busRead32(core,strtoul(a,0,16)); unsigned ad=p+strtoul(b,0,16); printf("R: %x:",ad); for(int i=0;i<n;i++)printf(" %02x",core->busRead8(core,ad+i)); printf("\n");}
  else if(sscanf(l,"writepb %63s %63s %63s",a,b,b+64)==3){ unsigned p=core->busRead32(core,strtoul(a,0,16)); core->busWrite8(core,p+strtoul(b,0,16),strtoul(b+64,0,16)&0xff);}
  else if(sscanf(l,"writep %63s %63s %63s",a,b,b+64)==3){ unsigned p=core->busRead32(core,strtoul(a,0,16)); unsigned ad=p+strtoul(b,0,16); unsigned v=strtoul(b+64,0,16); core->busWrite8(core,ad,v&0xff); core->busWrite8(core,ad+1,(v>>8)&0xff);}
  else if(sscanf(l,"write %63s %63s",a,b)==2){ unsigned ad=strtoul(a,0,16); unsigned v=strtoul(b,0,16); core->busWrite8(core,ad,v);}
  else if(sscanf(l,"read %63s %d",a,&n)==2){ unsigned ad=strtoul(a,0,16); printf("R: %s:",a); for(int i=0;i<n;i++)printf(" %02x",core->busRead8(core,ad+i)); printf("\n");}
 }
 return 0;}
