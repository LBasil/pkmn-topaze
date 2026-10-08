from play import run
import os
import os
S=os.environ.get('TOPAZE_STATES','./states/')
def walk(d,n): return ['key %s %d'%(d,16*n-2),'run 4']
def pos(): return 'readp 03005008 0 6'
def fromstate(name,L,**k): return run(['run 2','ls '+S+name+'.ss','run 2']+L,**k)
from PIL import Image
def sheet(prefix,n,out,cols=2):
    ims=[Image.open('%s%d.png'%(prefix,i)).resize((240,160)) for i in range(n)]
    rows=(n+cols-1)//cols
    W=Image.new('RGB',(240*cols,160*rows));[W.paste(im,(240*(i%cols),160*(i//cols))) for i,im in enumerate(ims)];W.save(out)
def mash(n,every,prefix,gap=60):
    L=[];k=0
    for i in range(n):
        L+=['key A 4','run %d'%gap]
        if (i+1)%every==0: L+=['shot %s%d.ppm'%(prefix,k)]; k+=1
    return L,k
