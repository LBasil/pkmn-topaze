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
import fog_tiles as FT
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

conns=connections()
_L=mapkit.layouts();_have={(a,dr,b) for a,dr,b,_ in conns}
for a,d in MAPS.items():
    for c in d.get('connections') or []:
        b=ID2NAME.get(c['map'])
        if not b or c['direction'] not in OPP or (a,c['direction'],b) in _have: continue
        la,lb=_L[d['layout']],_L[MAPS[b]['layout']]
        if (la['primary_tileset'],la['secondary_tileset'])==(lb['primary_tileset'],lb['secondary_tileset']): continue
        if {a,b}=={'PalletTown','Route1'}: continue     # raccord valide par Basil (tuiles identiques)
        conns.append((a,c['direction'],b,c['offset']))
# 1) on repart toujours des fichiers d'origine des tilesets secondaires concernes
for a,dr,b,off in conns:
    for n in (a,b): FT.restore_base(_L[MAPS[n]['layout']]['secondary_tileset'])
_CTX={}
def ctx(lid,end):
    k=(lid,end and (tuple(end[0]),tuple(end[1])))
    if k not in _CTX: _CTX[k]=FT.LayoutCtx(layout(lid),end)
    return _CTX[k]
class TSS:
    def __init__(s,name):
        s.name=name; ts=mapkit.Tileset(name); s.ts=ts
        s.n0=(ts.img.height//8)*(ts.img.width//8); s.m0=len(ts.metatiles)//16
        s.tiles=[];s.tkey={};s.metas=[];s.attrs=[];s.mkey={}
    def free_tiles(s): return FT.MAXSEC-s.n0-len(s.tiles)
    def free_metas(s): return FT.MAXSEC-s.m0-len(s.metas)
    def find_tile(s,idx):
        for hf in (0,1):
            for vf in (0,1):
                t=idx
                if hf: t=t[:,::-1]
                if vf: t=t[::-1,:]
                k=t.tobytes()
                if k in s.tkey: return s.tkey[k],hf,vf     # tuile T avec flips tels que flip(T)=idx... (voir add_tile)
        return None
    def add_tile(s,idx):
        f=s.find_tile(idx)
        if f: return f
        n=s.n0+len(s.tiles); s.tiles.append(idx.copy()); s.tkey[idx.tobytes()]=n
        return n,0,0
TS={}
def tss(name):
    if name not in TS: TS[name]=TSS(name)
    return TS[name]
jobs=[]
for k,(a,dr,b,off) in enumerate(conns):
    la,lb=MAPS[a]['layout'],MAPS[b]['layout']
    LA=layout(la);LB=layout(lb)
    CA=ctx(la,FT.RAMPS.get(la,{}).get(FT.DIRN[dr])); CB=ctx(lb,FT.RAMPS.get(lb,{}).get(FT.DIRN[OPP[dr]]))
    x0,y0,w,h=rect(LB.w,LB.h,dr)
    cnt=collections.Counter(LB.get(x,y)&0x3ff for y in range(y0,y0+h) for x in range(x0,x0+w))
    j=dict(k=k,a=a,b=b,dr=dr,la=la,lb=lb,LA=LA,LB=LB,CA=CA,CB=CB,rect=(x0,y0,w,h),cnt=cnt,S=tss(_L[la]['secondary_tileset']))
    mids=sorted(cnt)
    T={m:CB.render(m) for m in mids}
    blocks={}   # cle -> bloc (8,8,3)
    mblk={}
    for m in mids:
        ks=[]
        for q in range(4):
            y,x=(q//2)*8,(q%2)*8
            bl=T[m][y:y+8,x:x+8]; key=bl.astype(np.uint8).tobytes()
            blocks[key]=bl; ks.append(key)
        mblk[m]=ks
    keys=list(blocks)
    pool=FT.build_pool(CA)
    ex=FT.best_existing(pool,np.array([blocks[k_] for k_ in keys]))
    res={}
    for k_,(ee,ent) in zip(keys,ex):
        ef,bank,idx=FT.quantize(CA,blocks[k_])
        res[k_]=dict(ee=ee,ent=ent,ef=ef,bank=bank,idx=idx,choice=('E',ent),err=ee)
    j.update(T=T,mblk=mblk,res=res,pool=pool)
    jobs.append(j)
    print('analyse %d/%d %s->%s'%(k+1,len(conns),a,b),flush=True)
# 2) tuiles neuves : par gain decroissant dans la limite de la place du tileset
cands=[]
for j in jobs:
    use=collections.Counter()
    for m,c in j['cnt'].items():
        for k_ in j['mblk'][m]: use[k_]+=c
    for k_,r in j['res'].items():
        g=r['ee']-r['ef']
        if g>FT.GAIN_MIN: cands.append((g*use[k_],id(j),k_,j))
cands.sort(key=lambda t:-t[0])
for g,_,k_,j in cands:
    r=j['res'][k_]; S=j['S']
    f=S.find_tile(r['idx'])
    if f is None:
        if S.free_tiles()<=0: continue
        f=S.add_tile(r['idx'])
    n,hf,vf=f
    # find_tile renvoie (T,hf,vf) avec flip(idx)=T : l'entree utilise donc les memes flips
    r['choice']=('F',(640+n,hf,vf,r['bank'])); r['err']=r['ef']
# 3) metatuiles
def entry(e): return (e[0]&0x3ff)|(e[1]<<10)|(e[2]<<11)|(e[3]<<12)
def piece(C,ch,r):
    kind,(tid,hf,vf,bank)=ch
    if kind=='F': t=r['idx']
    else: t=C.tile(tid)
    if kind=='F' and (hf or vf):
        pass
    t2=t
    if kind=='E':
        if hf: t2=t2[:,::-1]
        if vf: t2=t2[::-1,:]
    return C.pals[bank][t2].astype(np.float32)
out=[];tab=[];dbg=[];stat=[]
for j in jobs:
    CA,CB,S,LA,LB=j['CA'],j['CB'],j['S'],j['LA'],j['LB']
    x0,y0,w,h=j['rect']; mm={}   # mid voisin -> (mid nouveau, bloque, image)
    used=[m for m in sorted(set(used_ids(LA))) if CA.valid(m)]
    exr={}
    def exrender(m):
        if m not in exr: exr[m]=CA.render(m)
        return exr[m]
    for m in sorted(j['cnt'],key=lambda m:-j['cnt'][m]):
        T=j['T'][m]; attrB=CB.attr(m)&~FT.LAYER_MASK
        chs=[j['res'][k_] for k_ in j['mblk'][m]]
        comp=np.zeros((16,16,3),np.float32)
        for q,r in enumerate(chs):
            y,x=(q//2)*8,(q%2)*8; comp[y:y+8,x:x+8]=piece(CA,r['choice'],r)
        Ec=float(((comp-T)**2).sum(2).mean())
        # metatuile existante equivalente (memes attributs) ?
        bm=None;Em=1e18
        for c in used:
            if (CA.attr(c)&~FT.LAYER_MASK)!=attrB: continue
            e=float(((exrender(c)-T)**2).sum(2).mean())
            if e<Em: Em=e;bm=c
        if bm is not None and Em<=Ec+60:
            mm[m]=(bm,False,exrender(bm),Em); continue
        ents=tuple(entry(r['choice'][1]) for r in chs)+(0,0,0,0)
        key=(ents,attrB)
        if key in S.mkey: mm[m]=(S.mkey[key],False,comp,Ec); continue
        if S.free_metas()>0 and Ec<(Em if bm is not None else 1e18):
            nid=640+S.m0+len(S.metas); S.metas.append(list(ents)); S.attrs.append(attrB); S.mkey[key]=nid
            mm[m]=(nid,False,comp,Ec); continue
        if bm is not None:
            mm[m]=(bm,False,exrender(bm),Em); continue
        # repli : metatuile la plus ressemblante de comportement compatible (ancienne methode)
        best,blk=translate(LA,LB,m|0,{})
        mm[m]=(best,blk,exrender(best) if CA.valid(best) else comp,float('nan'))
    j['mm']=mm
for S in TS.values():
    FT.write_tileset(S.ts,S.tiles,S.metas,S.attrs)
    print('%-28s +%3d tuiles (%d/384)  +%3d metatuiles (%d/384)'%(S.name,len(S.tiles),S.n0+len(S.tiles),len(S.metas),S.m0+len(S.metas)))
for j in jobs:
    k,a,b,LA,LB=j['k'],j['a'],j['b'],j['LA'],j['LB']
    x0,y0,w,h=j['rect']; mm=j['mm']; data=[]; tot=0.0;nn=0
    for y in range(y0,y0+h):
        for x in range(x0,x0+w):
            v=LB.get(x,y); nid,blk,_,e=mm[v&0x3ff]
            coll=(v>>10)&3
            if blk: coll=1
            data.append(nid|(coll<<10)|((v>>12)<<12))
            if e==e: tot+=e; nn+=1
    j['mean']=tot/max(1,nn)
    nm='sFogStrip%d'%k
    out.append('static const u16 %s[] = {%s};\n'%(nm,','.join(str(d) for d in data)))
    tab.append('    {%s, %s, %d, %d, %d, %d, %s},\n'%(MAPS[a]['layout'],MAPS[b]['layout'],x0,y0,w,h,nm))
    stat.append((j['mean'],a,j['dr'],b,sum(1 for m in mm.values() if m[0]>=640+j['S'].m0),sum(1 for m in mm.values() if m[1] or m[3]!=m[3])))
    if DEBUG:
        im1=Image.new('RGB',(w*16,h*16));im2=Image.new('RGB',(w*16,h*16))
        for i,v in enumerate(data):
            xx,yy=i%w,i//w
            im1.paste(j['CB'].L.metatile_img(LB.get(x0+xx,y0+yy)&0x3ff).convert('RGB'),(xx*16,yy*16))
            mid0=LB.get(x0+xx,y0+yy)&0x3ff
            im2.paste(Image.fromarray(np.clip(mm[mid0][2],0,255).astype(np.uint8),'RGB'),(xx*16,yy*16))
        dbg.append((k,a,b,im1,im2))
hdr='// genere par docs/topaze/fog_strips.py : bande (8 cases) de la carte voisine (vraie forme, requantifiee dans les palettes de la carte courante)\nstruct TopazeFogStrip { u16 layoutA; u16 layoutB; s16 x0; s16 y0; s16 w; s16 h; const u16 *data; };\n'
open(R+'include/topaze_fog_strips.h','w').write(hdr+''.join(out)+'static const struct TopazeFogStrip sTopazeFogStrips[] = {\n'+''.join(tab)+'    {0xFFFF, 0xFFFF, 0, 0, 0, 0, NULL},\n};\n')
print(len(conns),'bandes')
for s_ in sorted(stat,reverse=True): print('err moy %7.1f  %-26s %-5s %-26s neuves %2d repli %2d'%s_)
if DEBUG:
    os.makedirs('/tmp/fogdbg',exist_ok=True)
    for k,a,b,i1,i2 in dbg:
        W=max(i1.width,i2.width); M=Image.new('RGB',(W,i1.height+i2.height+4),(255,0,255)); M.paste(i1,(0,0)); M.paste(i2,(0,i1.height+4)); M.save('/tmp/fogdbg/%02d_%s_%s.png'%(k,a,b))
