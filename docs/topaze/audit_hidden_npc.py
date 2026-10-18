#!/usr/bin/env python3
"""Cherche les PNJ dont la case a une couche haute opaque (type NORMAL) : le sprite est cache sous le decor."""
import sys,json,glob,os,struct
sys.path.insert(0,'tools/topaze/maps'); import mapkit
LY=mapkit.layouts(); cache={}
def attr(L,mid):
    ts,i=(L.prim,mid) if mid<640 else (L.sec,mid-640)
    a=open(os.path.join(ts.d,'metatile_attributes.bin'),'rb').read()
    return struct.unpack_from('<I',a,i*4)[0] if i*4<len(a) else 0
def cover(L,mid):
    ts,idx=(L.prim,mid) if mid<640 else (L.sec,mid-640)
    if (idx+1)*16>len(ts.metatiles): return 0
    ents=struct.unpack_from('<8H',ts.metatiles,idx*16); n=0
    for e in ents[4:]:
        tid=e&0x3ff; src=L.prim if tid<640 else L.sec; t=tid if tid<640 else tid-640
        tw=src.img.width//8
        if (t//tw+1)*8>src.img.height: continue
        tile=src.img.crop(((t%tw)*8,(t//tw)*8,(t%tw)*8+8,(t//tw)*8+8)); px=tile.load()
        n+=sum(1 for y in range(8) for x in range(8) if px[x,y]!=0)
    return n/(4*64)
for f in sorted(glob.glob('data/maps/*/map.json')):
    j=json.load(open(f)); n=os.path.basename(os.path.dirname(f))
    if j['layout'] not in LY: continue
    try: L=cache.get(j['layout']) or mapkit.Layout(j['layout'])
    except Exception: continue
    cache[j['layout']]=L
    for i,o in enumerate(j.get('object_events',[])):
        g=o['graphics_id']
        if g in ('OBJ_EVENT_GFX_ITEM_BALL',) or not g.startswith('OBJ_EVENT_GFX') or 'VAR' in g: continue
        x,y=o['x'],o['y']
        if not(0<=x<L.w and 0<=y<L.h): continue
        mid=L.get(x,y)&0x3ff; a=attr(L,mid)
        if (a>>29)&3!=0: continue
        c=cover(L,mid)
        if c>0.3: print('%s obj%d (%d,%d) %s mid %x couverture haute %.0f%%'%(n,i,x,y,g[14:],mid,c*100))
