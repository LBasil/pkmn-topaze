#!/usr/bin/env python3
"""Bibliotheque de fog_strips.py : 'augmentation' des tilesets secondaires pour que la bande de la carte voisine
(8 cases) soit dessinee avec la VRAIE forme de la carte voisine, requantifiee dans les palettes de la carte courante.

Principe (voir ARCHITECTURE.md, section raccords) :
  - pour chaque case de la bande, on rend la metatuile voisine (16x16, ses palettes passees dans sa rampe de raccord a pleine force) ;
  - on la decoupe en 4 blocs 8x8 ; chaque bloc est dessine soit avec une tuile deja presente (primaire/secondaire, n'importe quelle
    palette, flips), soit avec une NOUVELLE tuile ajoutee a la fin du tileset secondaire (couleurs requantifiees dans la meilleure
    palette de la carte courante, rampe de la carte courante a pleine force) ;
  - la metatuile est (si besoin) ajoutee a la fin du tileset secondaire : couche basse = les 4 blocs, couche haute vide,
    attributs = ceux de la metatuile voisine (comportement exact).
Les fichiers d'origine des tilesets sont conserves dans docs/topaze/fogbase/ (le script repart toujours de ces fichiers : idempotent)."""
import os,re,struct,shutil,collections
import numpy as np
from PIL import Image
from junction_lib import *

BASE=R+'docs/topaze/fogbase/'
DIRN={'up':0,'down':1,'left':2,'right':3}
LAYER_MASK=0x60000000
PLACE_MIN=40          # erreur moyenne/pixel au-dela de laquelle une palette voisine merite une banque libre
REUSE_TOL=60          # ecart d'erreur tolere pour reutiliser une tuile deja creee
GAIN_MIN=150           # gain d'erreur (moyenne/pixel, somme RVB) mini pour creer une tuile plutot que reutiliser une existante
MAXSEC=384

# ---------------------------------------------------------------- rampes
def load_ramps():
    t=open(R+'include/topaze_ramps.h').read(); out={}
    for m in re.finditer(r'\{ (LAYOUT_\w+), (\d+), \{(.*?) \} \}, //',t):
        ends={}
        for e in re.finditer(r'\{(\d), \{(-?\d+),(-?\d+),(-?\d+)\}, \{(-?\d+),(-?\d+),(-?\d+)\}\}',m.group(3)):
            v=[int(x) for x in e.groups()]; ends[v[0]]=(v[1:4],v[4:7])
        out[m.group(1)]=ends
    return out
RAMPS=load_ramps()
def ramp_pal(pal,end):
    """pal : (16,3) uint8 ; end : (gain[3],bias[3]) ou None ; ramp a pleine force (q=16), couleur 0 intacte"""
    p=pal.astype(np.int32).copy()
    if end is None: return p
    g,b=end
    for i in range(1,16):
        for ch in range(3):
            o=int(p[i,ch])>>3
            v=((o*g[ch])>>8)+b[ch]
            p[i,ch]=max(0,min(31,v))*8
    return p

# ---------------------------------------------------------------- tilesets
def attrs(ts):
    b=open(os.path.join(ts.d,'metatile_attributes.bin'),'rb').read()
    return list(struct.unpack('<%dI'%(len(b)//4),b))
def tile_arrays(ts):
    a=np.asarray(ts.img,dtype=np.uint8); h,w=a.shape; out=[]
    for ty in range(h//8):
        for tx in range(w//8): out.append(a[ty*8:ty*8+8,tx*8:tx*8+8].copy())
    return out
class LayoutCtx:
    """layout + palettes (rampees ou non) + tuiles"""
    def __init__(self,L,end):
        self.L=L; self.end=end
        self.pals={}
        for b in range(13):
            ts=L.prim if b<7 else L.sec
            raw=np.array(ts.pals.get(b,[(255,0,255)]*16),dtype=np.uint8)
            self.pals[b]=ramp_pal(raw,end)
        self.ptile=tile_arrays(L.prim); self.stile=tile_arrays(L.sec)
        self.pattr=attrs(L.prim); self.sattr=attrs(L.sec)
    def tile(self,t):
        if t<640: return self.ptile[t] if t<len(self.ptile) else None
        k=t-640; return self.stile[k] if k<len(self.stile) else None
    def attr(self,mid):
        if mid<640: return self.pattr[mid] if mid<len(self.pattr) else 0
        k=mid-640; return self.sattr[k] if k<len(self.sattr) else 0
    def valid(self,mid):
        if mid<640: return mid<len(self.L.prim.metatiles)//16
        return mid-640<len(self.L.sec.metatiles)//16
    def render(self,mid,extra=None):
        """metatuile -> (16,16,3) float32, fond noir (comme mapkit)"""
        ts=self.L.prim if mid<640 else self.L.sec
        idx=mid if mid<640 else mid-640
        raw=ts.metatiles[idx*16:idx*16+16]
        ents=struct.unpack('<8H',raw)
        im=np.zeros((16,16,3),dtype=np.float32)
        for layer in range(2):
            for q in range(4):
                e=ents[layer*4+q]; tid,hf,vf,pal=e&0x3ff,(e>>10)&1,(e>>11)&1,e>>12
                t=self.tile(tid)
                if t is None: continue
                if hf: t=t[:,::-1]
                if vf: t=t[::-1,:]
                p=self.pals.get(pal)
                if p is None: p=np.array([(255,0,255)]*16)
                rgb=p[t].astype(np.float32)
                if layer==1:
                    m=(t!=0)[:,:,None]
                else: m=np.ones((8,8,1),bool)
                y0,x0=(q//2)*8,(q%2)*8
                im[y0:y0+8,x0:x0+8]=np.where(m,rgb,im[y0:y0+8,x0:x0+8])
        return im

def sec_dir_files(ts): return [os.path.join(ts.d,f) for f in ('tiles.png','metatiles.bin','metatile_attributes.bin')]
def restore_base(tsname):
    d=mapkit.ts_dir(tsname); b=BASE+os.path.basename(d)+'/'
    os.makedirs(b,exist_ok=True)
    for f in ('tiles.png','metatiles.bin','metatile_attributes.bin'):
        if not os.path.exists(b+f): shutil.copy(os.path.join(d,f),b+f)
        else: shutil.copy(b+f,os.path.join(d,f))

def write_tileset(ts,metas):
    """metas : dict emplacement (0..383) -> (8 entrees u16, attribut u32) ; ecrase ou ajoute des metatuiles (le png n'est plus modifie :
    les tuiles neuves sont chargees a l'execution dans des cases de VRAM libres, voir TopazeLoadFogTiles dans src/fieldmap.c)"""
    d=ts.d; b=BASE+os.path.basename(d)+'/'
    mt=bytearray(open(b+'metatiles.bin','rb').read()); at=bytearray(open(b+'metatile_attributes.bin','rb').read())
    top=max([len(mt)//16]+[k+1 for k in metas])
    mt+=bytes(16*top-len(mt)); at+=bytes(4*top-len(at))
    for k,(ents,attr) in metas.items():
        mt[k*16:k*16+16]=struct.pack('<8H',*ents); at[k*4:k*4+4]=struct.pack('<I',attr)
    open(d+'/metatiles.bin','wb').write(bytes(mt)); open(d+'/metatile_attributes.bin','wb').write(bytes(at))

ANIM_SEC={'gTileset_CeladonCity':range(104,112),'gTileset_SilphCo':range(336,344),'gTileset_MtEmber':range(256,264),'gTileset_VermilionGym':range(240,247),'gTileset_CeladonGym':range(99,103)}
def free_sec_tiles(ts,name):
    """numeros de tuiles du tileset secondaire non referencees par ses metatuiles (reutilisables) + place a la fin"""
    n0=(ts.img.height//8)*(ts.img.width//8)
    ref=set()
    for i in range(len(ts.metatiles)//16):
        for e in struct.unpack('<8H',ts.metatiles[i*16:i*16+16]):
            t=e&0x3ff
            if t>=640: ref.add(t-640)
    for r in ANIM_SEC.get(name,[]): ref.add(r)
    free=[k for k in range(n0) if k not in ref]+list(range(n0,MAXSEC))
    return free,n0

# ---------------------------------------------------------------- banques
def banks_used(C,mids):
    used=set(); L=C.L
    for m in mids:
        ts=L.prim if m<640 else L.sec; i=m if m<640 else m-640
        if i*16+16>len(ts.metatiles): continue
        for e in struct.unpack('<8H',ts.metatiles[i*16:i*16+16]):
            t=C.tile(e&0x3ff)
            if t is not None and t.any(): used.add(e>>12)
    return used

# ---------------------------------------------------------------- pool de tuiles existantes (avec transparence)
PEN=4000.0
def build_pool(C,eff,excl=()):
    ids=[];rend=[];msk=[]
    ntiles=[(t,C.tile(t)) for t in range(0,640) if t not in excl]+[(640+k,C.stile[k]) for k in range(len(C.stile)) if (640+k) not in excl]
    for tid,t in ntiles:
        if t is None: continue
        for hf in (0,1):
            for vf in (0,1):
                tt=t
                if hf: tt=tt[:,::-1]
                if vf: tt=tt[::-1,:]
                m=(tt!=0).reshape(-1)
                for b in range(13):
                    rend.append(eff[b][tt].astype(np.float32).reshape(64,3)); ids.append((tid,hf,vf,b)); msk.append(m)
    return ids,np.array(rend,dtype=np.float32),np.array(msk,dtype=np.float32)
def best_existing(pool,targets,tmasks):
    """targets (m,64,3), tmasks (m,64) bool -> liste (erreur/64, (tid,hf,vf,bank))"""
    ids,P,Pm=pool; n=len(ids)
    P2=(P*P).sum(2)                    # (n,64)
    Pf=P.reshape(n,-1)
    res=[]
    for i0 in range(0,len(targets),48):
        T=targets[i0:i0+48].astype(np.float32); W=tmasks[i0:i0+48].astype(np.float32)
        t1=W@P2.T
        t2=(W[:,:,None]*T).reshape(len(T),-1)@Pf.T
        t3=(W*(T*T).sum(2)).sum(1)
        ham=W@(1-Pm).T+(1-W)@Pm.T
        D=t1-2*t2+t3[:,None]+PEN*ham
        j=D.argmin(1)
        for k,jj in enumerate(j): res.append((max(0.0,float(D[k,jj]))/64.0,ids[jj]))
    return res
def quantize(eff,target,tmask):
    """target (8,8,3), tmask (8,8) bool -> (err/64, bank, idx (8,8) avec 0 pour les pixels transparents)"""
    px=target.reshape(-1,3).astype(np.float32); m=tmask.reshape(-1); best=None
    for b in range(13):
        pal=eff[b][1:16].astype(np.float32)
        D=((px[:,None,:]-pal[None,:,:])**2).sum(2)
        j=D.argmin(1); e=float((D[np.arange(64),j]*m).sum())/64.0
        if best is None or e<best[0]: best=(e,b,np.where(m,j+1,0).astype(np.uint8).reshape(8,8))
    return best
def flips(idx):
    for hf in (0,1):
        for vf in (0,1):
            t=idx
            if hf: t=t[:,::-1]
            if vf: t=t[::-1,:]
            yield hf,vf,t

# ---------------------------------------------------------------- fusion de palettes (banques libres)
def _cluster(cols,wts,k):
    """k-means pondere (couleurs (n,3), poids (n,)) -> centres (<=k,3), cout"""
    cols=np.asarray(cols,float); wts=np.asarray(wts,float); n=len(cols)
    if n<=k: return cols.copy(),0.0
    # init : couleur la plus lourde, puis la plus eloignee (ponderee)
    cen=[cols[int(wts.argmax())]]
    while len(cen)<k:
        d=np.min([((cols-c)**2).sum(1) for c in cen],axis=0)*np.sqrt(wts+1)
        cen.append(cols[int(d.argmax())])
    cen=np.array(cen)
    for _ in range(12):
        D=((cols[:,None,:]-cen[None,:,:])**2).sum(2); a=D.argmin(1)
        for i in range(k):
            m=a==i
            if m.any(): cen[i]=(cols[m]*wts[m,None]).sum(0)/wts[m].sum()
    D=((cols[:,None,:]-cen[None,:,:])**2).sum(2); a=D.argmin(1)
    return cen,float((D[np.arange(n),a]*wts).sum())
def merge_palettes(sets,nbanks):
    """sets : liste de (couleurs (n,3), poids (n,)) -> liste de <=nbanks tableaux (15,3) uint8 (multiples de 8)"""
    cur=[]
    for cols,w in sets:
        cen,c=_cluster(cols,w,15); cur.append([np.asarray(cols,float),np.asarray(w,float),c])
    def merged(a,b):
        cols=np.vstack([a[0],b[0]]); w=np.concatenate([a[1],b[1]])
        # fusion des couleurs quasi identiques (<= 1 pas de 5 bits par canal)
        keep=[];kw=[]
        for c,ww in zip(cols,w):
            for i,k in enumerate(keep):
                if ((c-k)**2).sum()<=192:
                    kw[i]+=ww; break
            else: keep.append(c.copy()); kw.append(ww)
        cen,cost=_cluster(keep,kw,15)
        return [np.array(keep),np.array(kw),0.0],cen,cost
    while len(cur)>nbanks:
        best=None
        for i in range(len(cur)):
            for j in range(i+1,len(cur)):
                m,cen,cost=merged(cur[i],cur[j]); inc=cost-cur[i][2]-cur[j][2]
                if best is None or inc<best[0]: best=(inc,i,j,m,cost)
        inc,i,j,m,cost=best; m[2]=cost
        cur=[c for k,c in enumerate(cur) if k not in(i,j)]+[m]
    out=[]
    for cols,w,c in cur:
        cen,_=_cluster(cols,w,15)
        cen=np.clip(np.round(cen/8.0)*8,0,248).astype(np.uint8)
        while len(cen)<15: cen=np.vstack([cen,cen[-1:]])
        out.append(cen)
    return out

def pool_from_tiles(eff,tiles):
    """tiles : liste (numero, idx (8,8)) -> pool au format de build_pool (ids=(numero,hf,vf,bank))"""
    arr=[];ids=[]
    for n,t in tiles:
        for hf,vf,tt in flips(t): arr.append(tt); ids.append((n,hf,vf))
    A=np.array(arr,dtype=np.uint8)
    E=np.array([eff[b] for b in range(13)],dtype=np.float32)       # (13,16,3)
    R=E[:,A,:]                                                       # (13,m,8,8,3)
    m=len(arr)
    P=R.transpose(1,0,2,3,4).reshape(m*13,64,3)
    Pm=np.repeat((A!=0).reshape(m,64).astype(np.float32),13,axis=0)
    pid=[(i[0],i[1],i[2],b) for i in ids for b in range(13)]
    return pid,P,Pm
