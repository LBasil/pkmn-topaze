#!/usr/bin/env python3
"""SEAFOAM ISLANDS -> volcano: recolor the secondary tileset palettes (ice blues -> basalt / ember ramp).
Idempotent through a backup marker file. Run from repo root."""
import os,re,colorsys
d='data/tilesets/secondary/seafoam_islands/palettes'
marker=d+'/.volcano_done'
if os.path.exists(marker): print('already applied'); raise SystemExit
RAMP=[(0.0,(10,6,10)),(0.35,(34,22,28)),(0.6,(58,36,38)),(0.8,(88,50,46)),(0.93,(138,70,48)),(1.0,(236,130,56))]
def ramp(l):
    for (a,ca),(b,cb) in zip(RAMP,RAMP[1:]):
        if l<=b:
            t=(l-a)/(b-a) if b>a else 0
            return tuple(int(round(ca[i]+(cb[i]-ca[i])*t)) for i in range(3))
    return RAMP[-1][1]
for i in range(6,13):
    p=f'{d}/{i:02d}.pal'
    if not os.path.exists(p): continue
    lines=open(p).read().split('\n')
    out=lines[:3]
    for ln in lines[3:]:
        m=re.match(r'^(\d+) (\d+) (\d+)$',ln.strip())
        if not m: out.append(ln); continue
        r,g,b=map(int,m.groups())
        if (r,g,b) in ((255,0,255),(0,0,0)): out.append(ln); continue
        l=(0.299*r+0.587*g+0.114*b)/255
        # blue-ish pixels (water/ice) -> lava glow, grey/white -> basalt
        h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
        c=ramp(l)
        if s>0.18 and 0.5<h<0.75: c=(min(255,int(ramp(min(1,l*1.05))[0]*1.5)),int(ramp(l)[1]*0.9),int(ramp(l)[2]*0.7))
        out.append('%d %d %d'%c)
    open(p,'w').write('\n'.join(out))
open(marker,'w').write('done\n')
print('recolored')
