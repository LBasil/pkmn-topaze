#!/usr/bin/env python3
# Recolore la Route 22 (teintes vertes/turquoise -> bleu nuit de Jadielle). NON re-executable (ecrit les .pal en place).
import colorsys,sys
def rd(p):
    L=open(p).read().split(); n=int(L[2]); return [tuple(int(x) for x in L[3+3*i:6+3*i]) for i in range(n)]
def wr(p,cols):
    open(p,'w').write('JASC-PAL\r\n0100\r\n%d\r\n'%len(cols)+''.join('%d %d %d\r\n'%c for c in cols))
def conv(c):
    r,g,b=c; h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255); h*=360
    if s<0.12 or not (70<=h<=200): return c
    h=232; s=min(s*1.15+0.08,0.6); v=v*0.85
    r,g,b=colorsys.hsv_to_rgb(h/360,min(s,1),min(v,1)); return (round(r*255),round(g*255),round(b*255))
for d,idx in (('primary/general_opalroad',range(0,7)),('secondary/viridian_pepite',range(7,13))):
    for i in idx:
        p='data/tilesets/%s/palettes/%02d.pal'%(d,i)
        c=rd(p); wr(p,[c[0]]+[conv(x) for x in c[1:]])
