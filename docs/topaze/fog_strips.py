#!/usr/bin/env python3
"""Raccords de cartes sans 'effet de TP' (voir ARCHITECTURE.md, section raccords).
Pour chaque connexion dont les tilesets different (include/topaze_fog_pairs.h), calcule la bande de la carte voisine
(8 cases le long du bord commun) TRADUITE avec les metatuiles de la carte courante : pour chaque case voisine on garde
la collision/elevation reelle, et on prend la metatuile de la carte courante qui ressemble le plus (distance d'image)
parmi celles de meme comportement. Ecrit include/topaze_fog_strips.h (utilise par FillConnection, src/fieldmap.c).
Idempotent. Usage : python3 docs/topaze/fog_strips.py [--debug]"""
import sys,os,struct,collections,re
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
NBV=6      # profondeur verticale : l'ecran montre 5 rangees au-dela du bord
def rect(Bw,Bh,dr):
    if dr=='down': return (0,0,Bw,NBV)
    if dr=='up': return (0,Bh-NBV,Bw,NBV)
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
_CTX={}
def ctx(lid,end):
    k=(lid,end and (tuple(end[0]),tuple(end[1])))
    if k not in _CTX: _CTX[k]=FT.LayoutCtx(layout(lid),end)
    return _CTX[k]
# metatuiles que des scripts peuvent poser (setmetatile) : leurs banques ne sont jamais 'libres'
_ML={}
for m in re.finditer(r'#define (METATILE_\w+)\s+(0x[0-9A-Fa-f]+|\d+)',open(R+'include/constants/metatile_labels.h').read()): _ML[m.group(1)]=int(m.group(2),0)
def script_mids(lid):
    out=set()
    for n in LAY2MAP.get(lid,[]):
        f=R+'data/maps/%s/scripts.inc'%n
        if os.path.exists(f):
            for lab in re.findall(r'METATILE_\w+',open(f).read()):
                if lab in _ML: out.add(_ML[lab])
    return out
def layout_mids(lid):
    L=layout(lid); out={v&0x3ff for v in L.g}
    try:
        b=open(os.path.join(R,L.l['border_filepath']) if 'border_filepath' in L.l else os.devnull,'rb').read()
        out|={v&0x3ff for v in struct.unpack('<%dH'%(len(b)//2),b)}
    except Exception: pass
    return out|script_mids(lid)
# constantes METATILE_* citees dans le code/les scripts : jamais 'libres'
_CONST=set()
for root,_,fs in os.walk(R):
    if '/.git' in root or '/build' in root or '/tools' in root: continue
    for f in fs:
        if f.endswith(('.c','.h','.inc','.s','.json')) and f!='metatile_labels.h':
            try: t=open(os.path.join(root,f),errors='ignore').read()
            except Exception: continue
            if 'METATILE_' in t:
                for lab in re.findall(r'METATILE_\w+',t):
                    if lab in _ML: _CONST.add(_ML[lab])
_PF={}
def primary_free(CA):
    """numeros de tuiles du tileset primaire qu'aucune carte utilisant ce primaire ne reference (hors animations 416..511)"""
    name=CA.L.l['primary_tileset']
    if name in _PF: return _PF[name]
    ref=set(); sec_used=collections.defaultdict(set)
    for lid,l in _L.items():
        if l.get('primary_tileset')==name and 'blockdata_filepath' in l:
            try: sec_used[l['secondary_tileset']]|=layout_mids(lid)
            except Exception: pass
    for m in _CONST:
        for sname in list(sec_used): sec_used[sname].add(m)
    for sname,mids in sec_used.items():
        st=mapkit.Tileset(sname)
        for m in mids:
            t=CA.L.prim if m<640 else st; i=m if m<640 else m-640
            if i*16+16>len(t.metatiles): continue
            for e in struct.unpack('<8H',t.metatiles[i*16:i*16+16]):
                if (e&0x3ff)<640: ref.add(e&0x3ff)
    _PF[name]=[t for t in range(1,640) if t not in ref and not (416<=t<512)]
    return _PF[name]
class LSS:
    """une carte (layout) : cases de tuiles libres de la VRAM secondaire (640..1023) pour les tuiles neuves chargees a l'execution"""
    def __init__(s,lid,CA):
        mids=layout_mids(lid)|_CONST; ref=set()
        for m in mids:
            ts=CA.L.prim if m<640 else CA.L.sec; i=m if m<640 else m-640
            if i*16+16>len(ts.metatiles): continue
            for e in struct.unpack('<8H',ts.metatiles[i*16:i*16+16]):
                if (e&0x3ff)>=640: ref.add(e&0x3ff)
        for r in FT.ANIM_SEC.get(CA.L.l['secondary_tileset'],[]): ref.add(640+r)
        fr=sorted(set(primary_free(CA))|{t for t in range(640,1024) if t not in ref}); s.free0=set(fr)
        runs=[];cur=[]
        for t in fr:
            if cur and t==cur[-1]+1: cur.append(t)
            else:
                if cur: runs.append(cur)
                cur=[t]
        if cur: runs.append(cur)
        runs.sort(key=lambda r:-len(r))      # on remplit d'abord les plus longs blocs : moins de copies DMA a l'execution
        s.free=[t for r in runs for t in r]
        s.data={};s.tkey={}
        s.mfree0=[m for m in range(640,1024) if m not in mids]     # metatuiles non utilisees par cette carte : leurs definitions sont remplacees a l'execution
        s.mfree=list(s.mfree0); s.metas={};s.mkey={}
    def alloc(s,ents,attr):
        if not s.mfree: return None
        k=s.mfree.pop(0); s.metas[k]=(ents,attr); return k
    def find_new(s,idx):
        for hf,vf,t in FT.flips(idx):
            k=t.tobytes()
            if k in s.tkey: return s.tkey[k],hf,vf
        return None
    def add_new(s,idx):
        f=s.find_new(idx)
        if f: return f
        if not s.free: return None
        n=s.free.pop(0); s.data[n]=idx.copy(); s.tkey[idx.tobytes()]=n
        return n,0,0
LS={}
def lss(lid,CA):
    if lid not in LS: LS[lid]=LSS(lid,CA)
    return LS[lid]
_EXT={}
def exist_tiles(CA,excl=()):
    """tuiles existantes de la carte A par contenu d'indices -> (id,hf,vf)"""
    k=id(CA)
    if k not in _EXT:
        d={}
        for tid in [t for t in range(640) if t not in excl]+[640+i for i in range(len(CA.stile)) if (640+i) not in excl]:
            t=CA.tile(tid)
            if t is None: continue
            for hf,vf,tt in FT.flips(t):
                d.setdefault(tt.tobytes(),(tid,hf,vf))
        _EXT[k]=d
    return _EXT[k]
# 2) groupes (carte A, direction) : memes banques libres, memes palettes placees
groups=collections.OrderedDict()
for k,(a,dr,b,off) in enumerate(conns):
    groups.setdefault((MAPS[a]['layout'],dr),[]).append((k,a,dr,b,off))
GR=[]
for (la,dr),lst in groups.items():
    LA=layout(la); CA=ctx(la,FT.RAMPS.get(la,{}).get(FT.DIRN[dr]))
    used=FT.banks_used(CA,layout_mids(la)); F=sorted(set(range(13))-used)
    g=dict(la=la,dr=dr,LA=LA,CA=CA,F=F,LS=lss(la,CA),jobs=[])
    ents={}      # cle -> dict(idx,pal,w,nz)
    pals={}
    for (k,a,dr_,b,off) in lst:
        lb=MAPS[b]['layout']; LB=layout(lb); CB=ctx(lb,FT.RAMPS.get(lb,{}).get(FT.DIRN[OPP[dr]]))
        x0,y0,w,h=rect(LB.w,LB.h,dr)
        cnt=collections.Counter(LB.get(x,y)&0x3ff for y in range(y0,y0+h) for x in range(x0,x0+w))
        j=dict(k=k,a=a,b=b,LB=LB,CB=CB,rect=(x0,y0,w,h),cnt=cnt,T={m:CB.render(m) for m in cnt},ments={})
        for m,c in cnt.items():
            ts=LB.prim if m<640 else LB.sec; i=m if m<640 else m-640
            raw=struct.unpack('<8H',ts.metatiles[i*16:i*16+16]); lst2=[]
            for e in raw:
                tid,hf,vf,pb=e&0x3ff,(e>>10)&1,(e>>11)&1,e>>12
                t=CB.tile(tid)
                if t is None or not t.any(): lst2.append(None); continue
                t2=t
                if hf: t2=t2[:,::-1]
                if vf: t2=t2[::-1,:]
                pal=CB.pals[pb]; pk=pal[1:16].astype(np.uint8).tobytes()
                key=(t2.tobytes(),pk)
                if key not in ents: ents[key]=dict(idx=t2.copy(),pal=pal,pk=pk,w=0,nz=(t2!=0))
                ents[key]['w']+=c; lst2.append(key)
                pals.setdefault(pk,pal)
            j['ments'][m]=lst2
        g['jobs'].append(j)
    g['ents']=ents; g['pals']=pals
    GR.append(g)
print('%d groupes, %d connexions'%(len(GR),len(conns)),flush=True)
def entry_img(pal,idx): return pal[idx].astype(np.float32)
for gi,g in enumerate(GR):
    CA=g['CA'];ents=g['ents'];F=g['F']
    base_eff={b:CA.pals[b] for b in range(13)}
    keys=list(ents)
    T=np.array([entry_img(ents[k]['pal'],ents[k]['idx']) for k in keys],np.float32).reshape(len(keys),64,3) if keys else np.zeros((0,64,3),np.float32)
    M=np.array([ents[k]['nz'].reshape(-1) for k in keys],bool) if keys else np.zeros((0,64),bool)
    def evaluate(eff):
        pool=FT.build_pool(CA,eff,g['LS'].free0); ex=FT.best_existing(pool,T,M)
        out=[]
        for k,(ee,ent) in zip(keys,ex):
            ef,bank,idx=FT.quantize(eff,T[len(out)].reshape(8,8,3),ents[k]['nz'])
            out.append((ee,ent,ef,bank,idx))
        return out
    r0=evaluate(base_eff) if keys else []
    # palettes a placer dans les banques libres : on ne place que celles que les banques existantes rendent mal,
    # puis on fusionne les palettes proches (couleurs communes) jusqu'a tenir dans les banques libres
    ben=collections.Counter(); tot=collections.Counter()
    for k,(ee,ent,ef,bank,idx) in zip(keys,r0):
        e=ents[k]; npx=e['nz'].sum()/64.0
        ben[e['pk']]+=e['w']*min(ee,ef)*npx; tot[e['pk']]+=e['w']*npx
    bad=[pk for pk in ben if ben[pk]/max(tot[pk],1e-9)>FT.PLACE_MIN]
    sets=[]
    for pk in bad:
        pal=np.frombuffer(pk,np.uint8).reshape(15,3).astype(float); cnt=np.zeros(15)
        for k in keys:
            e=ents[k]
            if e['pk']==pk:
                for i in range(15): cnt[i]+=e['w']*(e['idx']==i+1).sum()
        sets.append((pal,cnt+1e-3))
    eff=dict(base_eff); placed={}
    if sets and F:
        banks=FT.merge_palettes(sets,len(F))
        for bank,cols in zip(F,banks):
            p=np.vstack([CA.pals[bank][0:1],cols]); eff[bank]=p; placed[bank]=cols.astype(np.uint8).tobytes()
    g['placed']=placed; g['eff']=eff
    r1=evaluate(eff) if keys else []
    for k,(ee,ent,ef,bank,idx) in zip(keys,r1):
        e=ents[k]; e.update(ee=ee,ent=ent,ef=ef,fbank=bank,fidx=idx,code=('E',ent),err=ee)
    print('groupe %d/%d %s %s : %d entrees, %d a placer, banques libres %s, placees %s'%(gi+1,len(GR),g['la'],g['dr'],len(keys),len(sets),F,sorted(placed)),flush=True)
# 3) tuiles neuves par ordre de gain
cands=[]
for gi,g in enumerate(GR):
    for k,e in g['ents'].items():
        gain=e['ee']-e['ef']
        if gain>FT.GAIN_MIN: cands.append((gain*e['w']*max(1,e['nz'].sum())/64.0,gi,k))
cands.sort(key=lambda t:-t[0])
nfail=0;FAILS={}
for gain,gi,k in cands:
    g=GR[gi]; e=g['ents'][k]; S=g['LS']
    idx=e['fidx']; bank=e['fbank']
    ex=exist_tiles(g['CA'],S.free0).get(idx.tobytes())
    if ex is not None:
        e['code']=('E',(ex[0],ex[1],ex[2],bank)); e['err']=e['ef']; continue
    f=S.find_new(idx)
    if f is None and S.data:
        # une tuile deja creee (pour une autre entree) qui convient presque aussi bien ?
        pool=FT.pool_from_tiles(g['eff'],list(S.data.items()))
        T=(e['pal'][e['idx']].astype(np.float32)).reshape(1,64,3)
        ee2,ent2=FT.best_existing(pool,T,e['nz'].reshape(1,64))[0]
        if ee2<=e['ef']+FT.REUSE_TOL:
            e['code']=('F',(ent2[0],ent2[1],ent2[2],ent2[3])); e['err']=ee2; continue
    f=S.add_new(idx)
    if f is None: nfail+=1; FAILS[g['la']+' '+g['dr']]=FAILS.get(g['la']+' '+g['dr'],0)+1; continue
    n,hf,vf=f
    e['code']=('F',(n,hf,vf,bank)); e['err']=e['ef']
print('tuiles neuves : %d candidates, %d sans place'%(len(cands),nfail),flush=True)
for k_,v_ in sorted(FAILS.items(),key=lambda t:-t[1]): print('   sans place:',k_,v_,'(cases libres de la carte: %d)'%len(LS[k_.split()[0]].free0))
# 4) metatuiles
def entry(c): return (c[0]&0x3ff)|(c[1]<<10)|(c[2]<<11)|(c[3]<<12)
def tile_of(CA,S,tid):
    if tid in S.data: return S.data[tid]
    return CA.tile(tid)
def render_ents(CA,S,eff,ents):
    im=np.zeros((16,16,3),np.float32)
    for layer in range(2):
        for q in range(4):
            e=ents[layer*4+q]; tid,hf,vf,pal=e&0x3ff,(e>>10)&1,(e>>11)&1,e>>12
            t=tile_of(CA,S,tid)
            if t is None: continue
            if hf: t=t[:,::-1]
            if vf: t=t[::-1,:]
            rgb=eff.get(pal,eff[0])[t].astype(np.float32)
            m=(t!=0)[:,:,None] if layer==1 else np.ones((8,8,1),bool)
            y0,x0=(q//2)*8,(q%2)*8
            im[y0:y0+8,x0:x0+8]=np.where(m,rgb,im[y0:y0+8,x0:x0+8])
    return im
stat=[];out=[];tab=[];dbg=[]
sid=0;strip_pal=[]
PLAN={}
for g in GR:
    CA,S,eff,LA=g['CA'],g['LS'],g['eff'],g['LA']
    used=[m for m in sorted(set(used_ids(LA))) if CA.valid(m)]
    exr={}
    def exrender(m,CA=CA,S=S,eff=eff,LA=LA,exr=exr):
        if m not in exr:
            ts=LA.prim if m<640 else LA.sec; i=m if m<640 else m-640
            exr[m]=render_ents(CA,S,eff,struct.unpack('<8H',ts.metatiles[i*16:i*16+16]))
        return exr[m]
    for j in g['jobs']:
        CB=j['CB']; j['mm']={}
        for m in sorted(j['cnt'],key=lambda m:-j['cnt'][m]):
            T=j['T'][m]; attrB=CB.attr(m)
            ents=tuple(0 if key is None else entry(g['ents'][key]['code'][1]) for key in j['ments'][m])
            comp=render_ents(CA,S,eff,ents)
            Ec=float(((comp-T)**2).sum(2).mean())
            bm=None;Em=1e18
            for c in used:
                if (CA.attr(c)&~FT.LAYER_MASK)!=(attrB&~FT.LAYER_MASK): continue
                e_=float(((exrender(c)-T)**2).sum(2).mean())
                if e_<Em: Em=e_;bm=c
            PLAN.setdefault(g['la'],[]).append(dict(g=g,j=j,m=m,ents=ents,attr=attrB,comp=comp,Ec=Ec,bm=bm,Em=Em,bimg=exrender(bm) if bm is not None else None,cnt=j['cnt'][m]))
def allocate(S,lid,tol):
    S.mfree=list(S.mfree0); S.metas={}; S.mkey={}; fails=0
    for it in sorted(PLAN[lid],key=lambda it:-it['cnt']):
        g,j,m=it['g'],it['j'],it['m']; mm=j['mm']
        if it['bm'] is not None and it['Em']<=it['Ec']+tol: mm[m]=(it['bm'],False,it['bimg'],it['Em']); continue
        key=(it['ents'],it['attr'])
        if key in S.mkey: mm[m]=(S.mkey[key],False,it['comp'],it['Ec']); continue
        nid=S.alloc(list(it['ents']),it['attr'])
        if nid is not None: S.mkey[key]=nid; mm[m]=(nid,False,it['comp'],it['Ec']); continue
        fails+=1
        if it['bm'] is not None: mm[m]=(it['bm'],False,it['bimg'],it['Em']); continue
        best,blk=translate(g['LA'],j['LB'],m,{})
        mm[m]=(best,blk,it['comp'],float('nan'))
    return fails
for lid,S in LS.items():
    if lid not in PLAN: continue
    for tol in (40,120,250,500,1000):
        f=allocate(S,lid,tol)
        if f==0: break
    if f or tol>40: print('%-34s tolerance %d, %d echecs'%(lid,tol,f))
tile_arrays={}
for lid,Lx in LS.items():
    ids=sorted(Lx.data)
    if not ids: continue
    # blocs de numeros consecutifs -> une copie DMA chacun
    runs=[];st=ids[0];n=1
    for a_,b_ in zip(ids,ids[1:]):
        if b_==a_+1: n+=1
        else: runs.append((st,n)); st=b_; n=1
    runs.append((st,n))
    words=[]
    for t in ids:
        px=Lx.data[t]; 
        for y in range(8):
            w=0
            for x in range(8): w|=int(px[y,x])<<(4*x)
            words.append(w)
    tile_arrays[lid]=(runs,words)
pal_arrays=[]
for g in GR:
    # palettes placees de ce groupe (bank, 15 couleurs BGR555)
    pl=sorted(g['placed'].items()); name='sFogPal%d'%len(pal_arrays)
    cols=[]
    for bank,pk in pl:
        p=np.frombuffer(pk,dtype=np.uint8).reshape(15,3)
        cols+=[(int(r)>>3)|((int(gg)>>3)<<5)|((int(bb)>>3)<<10) for r,gg,bb in p]
    g['palname']=name; g['npal']=len(pl)
    if pl:
        pal_arrays.append('static const u8 %sB[] = {%s};\nstatic const u16 %sC[] = {%s};\n'%(name,','.join(str(b) for b,_ in pl),name,','.join(str(c) for c in cols)))
    else: pal_arrays.append('')
    for j in g['jobs']:
        k,a,b,LB=j['k'],j['a'],j['b'],j['LB']
        x0,y0,w,h=j['rect']; mm=j['mm']; data=[]; tot=0.0;nn=0
        for y in range(y0,y0+h):
            for x in range(x0,x0+w):
                v=LB.get(x,y); nid,blk,_,e=mm[v&0x3ff]
                coll=(v>>10)&3
                if blk: coll=1
                data.append(nid|(coll<<10)|((v>>12)<<12))
                if e==e: tot+=e; nn+=1
        j['mean']=tot/max(1,nn); j['data']=data
        nm='sFogStrip%d'%k
        out.append('static const u16 %s[] = {%s};\n'%(nm,','.join(str(d) for d in data)))
        pn=('%sB, %sC'%(name,name)) if pl else 'NULL, NULL'
        tab.append((k,'    {%s, %s, %d, %d, %d, %d, %s, %d, %d, %s},\n'%(MAPS[a]['layout'],MAPS[b]['layout'],x0,y0,w,h,nm,FT.DIRN[g['dr']],len(pl),pn)))
        stat.append((j['mean'],a,g['dr'],b,len(pl),len(g['F']),sum(1 for m in mm.values() if m[1] or m[3]!=m[3])))
        if DEBUG:
            im1=Image.new('RGB',(w*16,h*16));im2=Image.new('RGB',(w*16,h*16))
            for i,v in enumerate(data):
                xx,yy=i%w,i//w; mid0=LB.get(x0+xx,y0+yy)&0x3ff
                im1.paste(Image.fromarray(np.clip(j['T'][mid0],0,255).astype(np.uint8),'RGB'),(xx*16,yy*16))
                im2.paste(Image.fromarray(np.clip(mm[mid0][2],0,255).astype(np.uint8),'RGB'),(xx*16,yy*16))
            dbg.append((k,a,b,im1,im2))
tab.sort()
hdr='// genere par docs/topaze/fog_strips.py : bande (8 cases) de la carte voisine (vraie forme) dessinee avec les tuiles/palettes de la carte courante\nstruct TopazeFogStrip { u16 layoutA; u16 layoutB; s16 x0; s16 y0; s16 w; s16 h; const u16 *data; u8 dir; u8 nPal; const u8 *palBank; const u16 *palCol; };\nstruct TopazeFogTileRun { u16 first; u16 count; u16 offset; };\nstruct TopazeFogTiles { u16 layoutId; u8 nRuns; const struct TopazeFogTileRun *runs; const u32 *data; };\nstruct TopazeFogMetas { u16 layoutId; u16 n; const u16 *ids; const u16 *ents; const u32 *attrs; };\n'
tl=[];tt=[]
for lid,(runs,words) in sorted(tile_arrays.items()):
    nm=lid.lower()
    off=0;rr=[]
    for st,n in runs: rr.append('{%d,%d,%d}'%(st,n,off)); off+=n*8
    tl.append('static const struct TopazeFogTileRun sFogRuns_%s[] = {%s};\nstatic const u32 sFogTileData_%s[] = {%s};\n'%(nm,','.join(rr),nm,','.join('0x%08X'%w for w in words)))
    tt.append('    {%s, %d, sFogRuns_%s, sFogTileData_%s},\n'%(lid,len(runs),nm,nm))
tilestab='static const struct TopazeFogTiles sTopazeFogTiles[] = {\n'+''.join(tt)+'    {0xFFFF, 0, NULL, NULL},\n};\n'
ml=[];mt=[]
for lid,Lx in sorted(LS.items()):
    if not Lx.metas: continue
    ks=sorted(Lx.metas); nm=lid.lower()
    ml.append('static const u16 sFogMetaIds_%s[] = {%s};\nstatic const u16 sFogMetaEnts_%s[] = {%s};\nstatic const u32 sFogMetaAttr_%s[] = {%s};\n'%(nm,','.join(str(k) for k in ks),nm,','.join(str(x) for k in ks for x in Lx.metas[k][0]),nm,','.join('0x%08X'%Lx.metas[k][1] for k in ks)))
    mt.append('    {%s, %d, sFogMetaIds_%s, sFogMetaEnts_%s, sFogMetaAttr_%s},\n'%(lid,len(ks),nm,nm,nm))
metastab='static const struct TopazeFogMetas sTopazeFogMetas[] = {\n'+''.join(mt)+'    {0xFFFF, 0, NULL, NULL, NULL},\n};\n'
open(R+'include/topaze_fog_strips.h','w').write(hdr+''.join(tl)+tilestab+''.join(ml)+metastab+''.join(pal_arrays)+''.join(out)+'static const struct TopazeFogStrip sTopazeFogStrips[] = {\n'+''.join(t[1] for t in tab)+'    {0xFFFF, 0xFFFF, 0, 0, 0, 0, NULL, 0, 0, NULL, NULL},\n};\n')
print(len(conns),'bandes')
for s_ in sorted(stat,reverse=True): print('err moy %7.1f  %-26s %-5s %-26s pal %d/%d repli %d'%s_)
if DEBUG:
    os.makedirs('/tmp/fogdbg',exist_ok=True)
    for k,a,b,i1,i2 in dbg:
        W=max(i1.width,i2.width); M=Image.new('RGB',(W,i1.height+i2.height+4),(255,0,255)); M.paste(i1,(0,0)); M.paste(i2,(0,i1.height+4)); M.save('/tmp/fogdbg/%02d_%s_%s.png'%(k,a,b))
if os.environ.get('DBGJOB'):
    k=int(os.environ['DBGJOB'])
    for g in GR:
        for j in g['jobs']:
            if j['k']==k:
                rows=sorted(((v[3],m,j['cnt'][m],v[0]) for m,v in j['mm'].items() if v[3]==v[3]),reverse=True)[:12]
                for r in rows: print('mid %4d cnt %3d -> %4d err %.0f'%(r[1],r[2],r[3],r[0]))
                for r in rows[:4]:
                    m=r[1]; print('--- mid',m,'attr',hex(j['CB'].attr(m)))
                    ents_=tuple(0 if key is None else entry(g['ents'][key]['code'][1]) for key in j['ments'][m])
                    comp_=render_ents(g['CA'],g['LS'],g['eff'],ents_)
                    print('ents',[hex(x) for x in ents_],'Ec',float(((comp_-j['T'][m])**2).sum(2).mean()))
                    for q in range(4):
                        y0,x0=(q//2)*8,(q%2)*8
                        print(' quad',q,float(((comp_-j['T'][m])[y0:y0+8,x0:x0+8]**2).sum(2).mean()))
                    for q,key in enumerate(j['ments'][m]):
                        if key: e=g['ents'][key]; print(q,e['code'],'ee',round(e['ee']),'ef',round(e['ef']),'nz',e['nz'].sum(),'w',e['w'],'err',round(e['err']))
