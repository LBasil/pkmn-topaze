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
def write_tileset(ts,new_tiles,new_metas,new_attrs):
    """ajoute tuiles (liste de (8,8) uint8), metatuiles (liste de 8 u16) et attributs au tileset secondaire ts"""
    d=ts.d; b=BASE+os.path.basename(d)+'/'
    img=Image.open(b+'tiles.png'); w,h=img.size; n0=(h//8)*(w//8)
    tot=n0+len(new_tiles); rows=(tot+15)//16
    out=Image.new('P',(w,rows*8),0); out.putpalette(img.getpalette()); out.paste(img,(0,0))
    px=np.array(out,dtype=np.uint8)
    for i,t in enumerate(new_tiles):
        k=n0+i; ty,tx=k//16,k%16; px[ty*8:ty*8+8,tx*8:tx*8+8]=t
    out2=Image.fromarray(px,'P'); out2.putpalette(img.getpalette()); out2.save(d+'/tiles.png')
    mt=open(b+'metatiles.bin','rb').read()+b''.join(struct.pack('<8H',*m) for m in new_metas)
    open(d+'/metatiles.bin','wb').write(mt)
    at=open(b+'metatile_attributes.bin','rb').read()+b''.join(struct.pack('<I',a) for a in new_attrs)
    open(d+'/metatile_attributes.bin','wb').write(at)

# ---------------------------------------------------------------- pool de tuiles existantes
def build_pool(C):
    """toutes les (tuile, flips, palette) existantes de la carte -> rendu RGB (8*8*3)"""
    ids=[];rend=[]
    ntiles=[(t,C.tile(t)) for t in range(0,640)]+[(640+k,C.stile[k]) for k in range(len(C.stile))]
    for tid,t in ntiles:
        if t is None: continue
        for hf in (0,1):
            for vf in (0,1):
                tt=t
                if hf: tt=tt[:,::-1]
                if vf: tt=tt[::-1,:]
                for b in range(13):
                    rend.append(C.pals[b][tt].astype(np.float32).reshape(-1)); ids.append((tid,hf,vf,b))
    return ids,np.array(rend,dtype=np.float32)
def best_existing(pool,targets):
    ids,P=pool; P2=(P*P).sum(1)
    T=targets.reshape(len(targets),-1).astype(np.float32); T2=(T*T).sum(1)
    res=[]
    for i0 in range(0,len(T),64):
        D=T2[i0:i0+64,None]+P2[None,:]-2*T[i0:i0+64]@P.T
        j=D.argmin(1)
        for k,jj in enumerate(j): res.append((max(0.0,float(D[k,jj]))/64.0,ids[jj]))
    return res
def quantize(C,block):
    """block (8,8,3) -> (err/pixel, bank, idx(8,8)) meilleure palette parmi 13, indices 1..15"""
    px=block.reshape(-1,3).astype(np.float32); best=None
    for b in range(13):
        pal=C.pals[b][1:16].astype(np.float32)
        D=((px[:,None,:]-pal[None,:,:])**2).sum(2)
        j=D.argmin(1); e=float(D[np.arange(64),j].sum())/64.0
        if best is None or e<best[0]: best=(e,b,(j+1).astype(np.uint8).reshape(8,8))
    return best
