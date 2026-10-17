#!/usr/bin/env python3
"""Raccords de cartes sans 'effet de TP' (voir ARCHITECTURE.md, section raccords).
Pour chaque connexion dont les tilesets different (include/topaze_fog_pairs.h), calcule la bande de la carte voisine
(8 cases le long du bord commun) TRADUITE avec les metatuiles de la carte courante : pour chaque case voisine on garde
la collision/elevation reelle, et on prend la metatuile de la carte courante qui ressemble le plus (distance d'image)
parmi celles de meme comportement. Ecrit include/topaze_fog_strips.h (utilise par FillConnection, src/fieldmap.c).
Idempotent. Usage : python3 docs/topaze/fog_strips.py [--debug]"""
import sys,os,struct,collections
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from junction_lib import *
from PIL import Image
DEBUG='--debug' in sys.argv
NB=8
def attrs(ts):
    b=open(os.path.join(ts.d,'metatile_attributes.bin'),'rb').read()
    return struct.unpack('<%dI'%(len(b)//4),b)
_LC={};_IMG={};_ATT={}
def layout(lid):
    if lid not in _LC: _LC[lid]=mapkit.Layout(lid)
    return _LC[lid]
def nmeta(L): return 640+len(L.sec.metatiles)//16 if len(L.prim.metatiles)//16<=640 else None
def beh(L,mid):
    key=(L.l['primary_tileset'],L.l['secondary_tileset'])
    if key not in _ATT: _ATT[key]=(attrs(L.prim),attrs(L.sec))
    p,s=_ATT[key]
    if mid<640: return (p[mid]&0x1ff) if mid<len(p) else 0
    k=mid-640; return (s[k]&0x1ff) if k<len(s) else 0
def valid(L,mid):
    if mid<640: return mid<len(L.prim.metatiles)//16
    return mid-640<len(L.sec.metatiles)//16
def img(L,mid):
    key=(L.l['primary_tileset'],L.l['secondary_tileset'],mid)
    if key not in _IMG:
        im=L.metatile_img(mid).convert('RGBA'); bg=Image.new('RGBA',(16,16),(0,0,0,255)); bg.alpha_composite(im)
        _IMG[key]=np.asarray(bg.convert('RGB'),dtype=np.float32).reshape(-1)
    return _IMG[key]
SPECIAL=lambda b: b==0x02 or 0x10<=b<=0x1f or b in(0x21,0x23) or 0x38<=b<=0x3f
_USED={}
def used_ids(L):
    key=(L.l['primary_tileset'],L.l['secondary_tileset'])
    if key not in _USED:
        c=collections.Counter()
        for lid,l in mapkit.layouts().items():
            if (l['primary_tileset'],l['secondary_tileset'])==key:
                for v in layout(lid).g: c[v&0x3ff]+=1
        _USED[key]=c
    return _USED[key]
_CAND={}
def candidates(L,b):
    """metatuiles de L dont le comportement est compatible avec celui (b) de la case voisine"""
    key=(L.l['primary_tileset'],L.l['secondary_tileset'],SPECIAL(b) and b)
    if key in _CAND: return _CAND[key]
    used=used_ids(L); out=[]
    for mid in sorted(used):
        if not valid(L,mid): continue
        bb=beh(L,mid)
        if SPECIAL(b):
            if bb==b: out.append(mid)
        elif not SPECIAL(bb) and bb in(0x00,0x01,0x08,0x20,0x30,0x31,0x32,0x33,0x34,0x35): out.append(mid)
    _CAND[key]=out; return out
def translate(LA,LB,vB,cache):
    mid=vB&0x3ff; coll=(vB>>10)&3; elev=vB>>12
    if mid in cache: return cache[mid]
    b=beh(LB,mid)
    cand=candidates(LA,b)
    blocked=False
    if not cand:
        cand=candidates(LA,0); blocked=True       # pas d'equivalent (eau absente...) : case infranchissable
    target=img(LB,mid)
    best=None;bd=1e18
    for c in cand:
        d=float(np.mean((img(LA,c)-target)**2))
        # on prefere (a distance egale) les metatuiles que la carte utilise beaucoup
        d*=1.0-0.02*min(10,np.log1p(used_ids(LA)[c]))
        if d<bd: bd=d;best=c
    # collision identique a celle de la carte voisine (on marche reellement dessus apres le passage)
    cache[mid]=(best,blocked)
    return cache[mid]
def rect(Bw,Bh,dr):
    if dr=='down': return (0,0,Bw,NB)
    if dr=='up': return (0,Bh-NB,Bw,NB)
    if dr=='left': return (Bw-NB,0,NB,Bh)
    return (0,0,NB,Bh)
out=[];tab=[];dbg=[]
conns=connections()
# connexions reelles dont les tilesets different et qui ne sont pas dans la liste des paires brouillees (sinon tuiles brouillees)
_L=mapkit.layouts();_have={(a,dr,b) for a,dr,b,_ in conns}
for a,d in MAPS.items():
    for c in d.get('connections') or []:
        b=ID2NAME.get(c['map'])
        if not b or c['direction'] not in OPP or (a,c['direction'],b) in _have: continue
        la,lb=_L[d['layout']],_L[MAPS[b]['layout']]
        if (la['primary_tileset'],la['secondary_tileset'])==(lb['primary_tileset'],lb['secondary_tileset']): continue
        if {a,b}=={'PalletTown','Route1'}: continue     # raccord valide par Basil (tuiles identiques)
        conns.append((a,c['direction'],b,c['offset']))
for k,(a,dr,b,off) in enumerate(conns):
    LA=layout(MAPS[a]['layout']);LB=layout(MAPS[b]['layout'])
    x0,y0,w,h=rect(LB.w,LB.h,dr)
    cache={};data=[]
    for y in range(y0,y0+h):
        for x in range(x0,x0+w):
            v=LB.get(x,y); mid,blk=translate(LA,LB,v,cache)
            coll=(v>>10)&3
            if blk: coll=1
            data.append(mid|(coll<<10)|((v>>12)<<12))
    nm='sFogStrip%d'%k
    out.append('static const u16 %s[] = {%s};\n'%(nm,','.join(str(d) for d in data)))
    tab.append('    {%s, %s, %d, %d, %d, %d, %s},\n'%(MAPS[a]['layout'],MAPS[b]['layout'],x0,y0,w,h,nm))
    if DEBUG:
        # rendu : bande reelle de B (art de B) | bande traduite (art de A)
        im1=Image.new('RGB',(w*16,h*16));im2=Image.new('RGB',(w*16,h*16))
        for i,v in enumerate(data):
            xx,yy=i%w,i//w
            im1.paste(LB.metatile_img(LB.get(x0+xx,y0+yy)&0x3ff).convert('RGB'),(xx*16,yy*16))
            im2.paste(LA.metatile_img(v&0x3ff).convert('RGB'),(xx*16,yy*16))
        dbg.append((k,a,b,im1,im2))
hdr='// genere par docs/topaze/fog_strips.py : bande (8 cases) de la carte voisine traduite avec les metatuiles de la carte courante\nstruct TopazeFogStrip { u16 layoutA; u16 layoutB; s16 x0; s16 y0; s16 w; s16 h; const u16 *data; };\n'
open(R+'include/topaze_fog_strips.h','w').write(hdr+''.join(out)+'static const struct TopazeFogStrip sTopazeFogStrips[] = {\n'+''.join(tab)+'    {0xFFFF, 0xFFFF, 0, 0, 0, 0, NULL},\n};\n')
print(len(conns),'bandes,',sum(len(d) for d in [o for o in out]),'octets de texte')
if DEBUG:
    os.makedirs('/tmp/fogdbg',exist_ok=True)
    for k,a,b,i1,i2 in dbg:
        W=max(i1.width,i2.width); M=Image.new('RGB',(W,i1.height+i2.height+4),(255,0,255)); M.paste(i1,(0,0)); M.paste(i2,(0,i1.height+4)); M.save('/tmp/fogdbg/%02d_%s_%s.png'%(k,a,b))
