#!/usr/bin/env python3
"""Degrades de palette aux raccords de cartes (voir ARCHITECTURE.md, section raccords).
Pour chaque connexion routiere dont les couleurs moyennes au bord different trop (>= SEUIL), la carte de type route
recoit, sur ce bord, une transformation de palette affine par canal (gain, biais) qui rapproche ses couleurs de celles de la
carte voisine (ville : cible = la ville ; route <-> route : cible = mi-chemin des deux). Le moteur (src/fieldmap.c,
TopazeRampApply) l'applique progressivement sur ZONE cases avant le bord, si bien qu'au passage il n'y a plus de saut de teinte.
Ecrit include/topaze_ramps.h. Idempotent. Usage : python3 docs/topaze/ramp_gen.py"""
import sys,os,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from PIL import Image
import maprender as MR
from junction_lib import *
SEUIL=40; ZONE=14; DEPTH=6
L={x['id']:x for x in json.load(open(R+'data/layouts/layouts.json'))['layouts'] if x.get('id')}
_I={}
def img(lid):
    if lid not in _I:
        f='/tmp/ramp_%s.png'%lid; MR.render(L[lid],f); _I[lid]=np.asarray(Image.open(f).convert('RGB'),dtype=float)
    return _I[lid]
def strip(A,dr,idx):
    h,w=A.shape[:2]
    if dr=='up': return A[0:DEPTH*16,idx[0]*16:(idx[-1]+1)*16]
    if dr=='down': return A[h-DEPTH*16:h,idx[0]*16:(idx[-1]+1)*16]
    if dr=='left': return A[idx[0]*16:(idx[-1]+1)*16,0:DEPTH*16]
    return A[idx[0]*16:(idx[-1]+1)*16,w-DEPTH*16:w]
def stats(s): p=s.reshape(-1,3); return p.mean(0),p.std(0)
def isroute(n): return MAPS[n].get('map_type')=='MAP_TYPE_ROUTE'
DIRN={'up':0,'down':1,'left':2,'right':3}
ends={}
for a,d in MAPS.items():
    for c in d.get('connections') or []:
        b=ID2NAME.get(c['map'])
        if not b or c['direction'] not in OPP or not isroute(a): continue
        dr=c['direction']; off=c['offset']; la,lb=d['layout'],MAPS[b]['layout']
        if la==lb: continue
        idx=overlap(a,dr,b,off)
        if len(idx)<2: continue
        idxb=[i-off for i in idx]
        sa=strip(img(la),dr,idx); sb=strip(img(lb),OPP[dr],idxb)
        ma,sda=stats(sa); mb,sdb=stats(sb)
        dist=float(np.abs(ma-mb).sum())
        if dist<SEUIL: continue
        if isroute(b): tm=(ma+mb)/2; ts=(sda+sdb)/2
        else: tm=mb; ts=sdb
        gain=np.clip(ts/np.maximum(sda,1),0.7,1.45)
        bias=tm-gain*ma
        g256=[int(round(x*256)) for x in gain]; b5=[int(max(-31,min(31,round(x/8)))) for x in bias]
        ends.setdefault(la,[]).append((DIRN[dr],g256,b5,a,b,round(dist)))
out=['// genere par docs/topaze/ramp_gen.py : transformation de palette (gain/256, biais en unites 5 bits) appliquee sur ZONE cases avant le bord','#define TOPAZE_RAMP_ZONE %d'%ZONE,
'struct TopazeRampEnd { u8 dir; s16 gain[3]; s8 bias[3]; };','struct TopazeRamp { u16 layoutId; u8 n; struct TopazeRampEnd e[3]; };','static const struct TopazeRamp sTopazeRamps[] = {']
for lid,es in sorted(ends.items()):
    es=es[:3]
    out.append('    { %s, %d, {'%(lid,len(es))+', '.join('{%d, {%d,%d,%d}, {%d,%d,%d}}'%(e[0],*e[1],*e[2]) for e in es)+' } }, // '+'; '.join('%s->%s d=%d'%(e[3],e[4],e[5]) for e in es))
out.append('    { 0xFFFF, 0, {} }','' ) if False else out.append('    { 0xFFFF, 0, {{0,{0,0,0},{0,0,0}}} },')
out.append('};')
open(R+'include/topaze_ramps.h','w').write('\n'.join(out)+'\n')
print(len(ends),'cartes')
for lid,es in sorted(ends.items()): print(lid,[(e[3],e[4],e[5]) for e in es])
