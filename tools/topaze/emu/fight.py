from pl import *
import sys
which=sys.argv[1]; keys=sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2] else []
sel=[]
for k in keys: sel+=['key %s 4'%k,'run 12']
fromstate('rivalbattle',['key A 4','run 70']*14+['run 120'])
L=['key A 4','run 50','key A 4','run 30']+sel+['shot m1.ppm','key A 4','run 120']
M,k=mash(60,4,'f',gap=60)
fromstate('rivalbattle',['key A 4','run 70']*14+['run 120']+L+M)
sheet('f',min(k,15),'ff.png',cols=5)
