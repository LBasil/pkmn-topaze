#!/usr/bin/env python3
"""Liste les warps qui relient deux cartes exterieures (ville/route) -> candidats a une connexion fluide."""
import json,glob,os
L={l.get('id'):l for l in json.load(open('data/layouts/layouts.json'))['layouts']}
M={}
for f in glob.glob('data/maps/*/map.json'):
    j=json.load(open(f)); M[j['id']]=(os.path.basename(os.path.dirname(f)),j)
OUT={'MAP_TYPE_TOWN','MAP_TYPE_CITY','MAP_TYPE_ROUTE','MAP_TYPE_OCEAN_ROUTE'}
def info(mid):
    n,j=M[mid]; l=L.get(j['layout']) or {}; return n,j,l
rows=[]
for mid,(n,j) in sorted(M.items()):
    if j.get('map_type') not in OUT: continue
    l=L.get(j['layout']); 
    if not l: continue
    W,H=l['width'],l['height']
    for i,w in enumerate(j.get('warp_events',[])):
        d=w['dest_map']
        if d not in M: continue
        dj=M[d][1]
        if dj.get('map_type') not in OUT: continue
        edge=w['x'] in (0,W-1) or w['y'] in (0,H-1)
        rows.append((n,i,w['x'],w['y'],W,H,M[d][0],edge,l['primary_tileset'],L[dj['layout']]['primary_tileset']))
print('Warps exterieur -> exterieur :',len(rows))
for r in rows: print('%-26s w%-2d (%2d,%2d) %2dx%-2d -> %-26s %s  %s -> %s'%(r[0],r[1],r[2],r[3],r[4],r[5],r[6],'BORD' if r[7] else 'int ',r[8].replace('gTileset_',''),r[9].replace('gTileset_','')))
