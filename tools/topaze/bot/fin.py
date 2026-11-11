import sys; sys.path.insert(0,'/tmp/gx')
from drive import *
from PIL import Image
ims=[]
for n,(g,m,x,y) in {'cer':(3,3,20,26),'tum':(2,111,12,12)}.items():
    e=Emu('/tmp/gx/dbg.gba'); print(n,goto(e,g,m,x,y)); e.run(150,0); e.shot('/tmp/gx/f_%s.png'%n); e.p.kill(); ims.append(Image.open('/tmp/gx/f_%s.png'%n))
s=Image.new('RGB',(sum(i.width for i in ims),ims[0].height)); x=0
for i in ims: s.paste(i,(x,0)); x+=i.width
s.save('/tmp/gx/fin.png')
