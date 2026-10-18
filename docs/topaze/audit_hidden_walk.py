#!/usr/bin/env python3
"""Cases praticables dont la couche haute opaque (type NORMAL) cacherait le joueur."""
import sys,os,struct,collections
sys.path.insert(0,'tools/topaze/maps'); import mapkit
src=open('docs/topaze/audit_hidden_npc.py').read().split("for f in sorted")[0]; exec(src)
used=set(l['id'] for l in LY.values() if 'id' in l)
for lid in sorted(LY):
    try: L=mapkit.Layout(lid)
    except Exception: continue
    c=collections.Counter(); ex={}
    for y in range(L.h):
        for x in range(L.w):
            v=L.get(x,y)
            if (v>>10)&3: continue
            mid=v&0x3ff
            if (attr(L,mid)>>29)&3: continue
            if (attr(L,mid)&0x1ff) in (0x60,0x61,0x62,0x63,0x64,0x65,0x66,0x67,0x68,0x69): pass
            k=cover(L,mid)
            if k>=0.9: c[mid]+=1; ex.setdefault(mid,(x,y))
    if c: print(lid,{hex(m):(n,ex[m]) for m,n in c.most_common(8)})
