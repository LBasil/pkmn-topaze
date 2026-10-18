#!/usr/bin/env python3
"""Metatuiles praticables (collision 0) du tileset secondaire dont la couche haute est un doublon opaque de la couche basse
(type NORMAL) : le joueur y marche 'sous' le decor. On vide la couche haute (elle ne servait qu'a cacher les sprites).
Usage: fix_covering_tops.py <dossier tileset secondaire> ..."""
import sys,os,struct,collections
sys.path.insert(0,'tools/topaze/maps'); import mapkit
src=open('docs/topaze/audit_hidden_npc.py').read().split("for f in sorted")[0]; exec(src)
for d in sys.argv[1:]:
    path=os.path.join(d,'metatiles.bin'); data=bytearray(open(path,'rb').read())
    walk=collections.Counter()
    for lid,l in LY.items():
        if 'id' not in l: continue
        try: L=mapkit.Layout(lid)
        except Exception: continue
        if os.path.abspath(L.sec.d)!=os.path.abspath(d): continue
        for y in range(L.h):
            for x in range(L.w):
                v=L.get(x,y)
                if not (v>>10)&3 and (v&0x3ff)>=640: walk[v&0x3ff]+=1
    fixed=[]
    for mid in sorted(walk):
        i=mid-640
        if (i+1)*16>len(data): continue
        e=list(struct.unpack_from('<8H',data,i*16))
        a=struct.unpack_from('<I',open(os.path.join(d,'metatile_attributes.bin'),'rb').read(),i*4)[0]
        if (a>>29)&3: continue
        if e[:4]==e[4:] and any(e[4:]):
            struct.pack_into('<8H',data,i*16,*e[:4],0,0,0,0); fixed.append(hex(mid))
    open(path,'wb').write(bytes(data)); print(d,len(fixed),fixed)
