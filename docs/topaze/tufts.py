#!/usr/bin/env python3
"""Ajoute les 'franges' de haut d'arbre (touffes 0xcc/0xcd) au-dessus des arbres qui n'ont pas de pied d'arbre au-dessus.
Un arbre = 2x2 metatiles; le pied (1dc/1dd...) porte en bas les touffes du haut de l'arbre suivant.
Usage: tufts.py ROUTE1|VIRIDIAN  (idempotent : repart des metatiles existants)"""
import struct, sys, json
TOPS = {0x1d4:(0xcc,0x2000,'L'),0x1d5:(0xcd,0x2000,'R'),0x200:(0xcc,0x6000,'L'),0x201:(0xcd,0x6000,'R'),
        0x282:(0xcc,0x8000,'L'),0x283:(0xcd,0x8000,'R'),0x286:(0xcc,0x3000,'L'),0x287:(0xcd,0x3000,'R')}
FOOTS = {0x1dc,0x1dd,0x284,0x285,0x288,0x289,0x202,0x203}
CFG = {
 'ROUTE1': dict(layout='LAYOUT_ROUTE1', bin='data/layouts/Route1/map.bin', W=26,
    prim='data/tilesets/primary/general_gradient', sec='data/tilesets/secondary/gradient_road', other_prims=['data/tilesets/primary/general_opal'],
    grounds={0x001,0x204,0x280,0x281}),
 'PALLET': dict(layout='LAYOUT_PALLET_TOWN', bin='data/layouts/PalletTown/map.bin', W=44,
    prim='data/tilesets/primary/general_emerald', sec='data/tilesets/secondary/petalburg_emerald', other_prims=[],
    grounds={0x001}, pad_to=523, pre=[(1,0xcc,0x2000,'L',523),(1,0xcd,0x2000,'R',524)]),
 'VIRIDIAN': dict(layout='LAYOUT_VIRIDIAN_CITY', bin='data/layouts/ViridianCity/map.bin', W=42,
    prim='data/tilesets/primary/general_opal', sec='data/tilesets/secondary/rustboro_opal', other_prims=[],
    grounds={0x280}),
}
def load(d):
    m=bytearray(open(d+'/metatiles.bin','rb').read()); a=bytearray(open(d+'/metatile_attributes.bin','rb').read()); return m,a
def save(d,m,a): open(d+'/metatiles.bin','wb').write(m); open(d+'/metatile_attributes.bin','wb').write(a)
def main(key):
    c=CFG[key]; W=c['W']
    d=bytearray(open(c['bin'],'rb').read()); H=len(d)//2//W
    raw=lambda x,y: struct.unpack_from('<H',d,(y*W+x)*2)[0]
    tsets={c['prim']:load(c['prim']),c['sec']:load(c['sec'])}
    for o in c['other_prims']: tsets[o]=load(o)
    for dd in (c['prim'],):
        m,a=tsets[dd]
        while len(m)//16<c.get('pad_to',0): m+=bytes(16); a+=bytes(4)
        tsets[dd]=(m,a)
    reg={}   # (ground,pal,side) -> metatile id
    def get_tuft(ground,tile,pal,side):
        k=(ground,tile,pal,side)
        if k in reg: return reg[k]
        # ground metatile in its tileset
        if ground<640: dirs=[c['prim']]+c['other_prims']; base=ground
        else: dirs=[c['sec']]; base=ground-640
        newid=None
        for dd in dirs:
            m,a=tsets[dd]
            ent=list(struct.unpack('<8H',m[base*16:base*16+16])); attr=a[base*4:base*4+4]
            idx=6 if side=='R' else 7
            assert (ent[idx]&0x3ff)==0, (hex(ground),ent)
            ent[idx]=tile|pal
            # cherche un doublon deja ajoute
            n=len(m)//16; found=None
            for j in range(n-1,max(n-40,-1),-1):
                if m[j*16:j*16+16]==struct.pack('<8H',*ent) and a[j*4:j*4+4]==attr: found=j;break
            if found is None:
                m+=struct.pack('<8H',*ent); a+=attr; found=n
            nid=found if ground<640 else 640+found
            if newid is not None and nid!=newid: raise SystemExit('index primaires desynchronises')
            newid=nid
        reg[k]=newid; return newid
    for (gr,t,pl,sd,want) in c.get('pre',[]):
        assert get_tuft(gr,t,pl,sd)==want, 'ids primaires non alignes'
    n=0
    for y in range(1,H):
        for x in range(W):
            v=raw(x,y); i=v&0x3ff
            if i not in TOPS: continue
            up=raw(x,y-1); ui=up&0x3ff
            if ui in FOOTS or ui not in c['grounds']: continue
            tile,pal,side=TOPS[i]
            nid=get_tuft(ui,tile,pal,side)
            struct.pack_into('<H',d,((y-1)*W+x)*2,(up&~0x3ff)|nid); n+=1
    for dd,(m,a) in tsets.items(): save(dd,m,a)
    open(c['bin'],'wb').write(d); print(key,'tufts poses:',n,'metatiles:',reg)
main(sys.argv[1])
