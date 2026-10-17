"""Bibliotheque commune pour les raccords de cartes (voir junction_flatten.py)."""
import json,glob,os,re,sys
sys.path.insert(0,'/home/claude/pkmn-topaze/tools/topaze/maps')
import mapkit
R='/home/claude/pkmn-topaze/'
MAPS={};LAY2MAP={};ID2NAME={}
for f in glob.glob(R+'data/maps/*/map.json'):
    d=json.load(open(f)); n=os.path.basename(os.path.dirname(f)); MAPS[n]=d; ID2NAME[d['id']]=n; LAY2MAP.setdefault(d['layout'],[]).append(n)
def fog_pairs():
    t=open(R+'include/topaze_fog_pairs.h').read()
    return set(re.findall(r'\{(LAYOUT_\w+), (LAYOUT_\w+)\}',t))
OPP={'up':'down','down':'up','left':'right','right':'left'}
def connections():
    """liste (mapA, dir, mapB, offset) pour les connexions dont la paire de layouts est brouillee"""
    fp=fog_pairs();out=[]
    for a,d in MAPS.items():
        for c in d.get('connections') or []:
            b=ID2NAME.get(c['map'])
            if not b or c['direction'] not in OPP: continue
            if (d['layout'],MAPS[b]['layout']) in fp: out.append((a,c['direction'],b,c['offset']))
    return out

D=8
def dims(n):
    l=mapkit.layouts()[MAPS[n]['layout']]; return l['width'],l['height']
def overlap(a,dr,b,off):
    """indices le long du bord (cote A) couverts par B"""
    aw,ah=dims(a); bw,bh=dims(b)
    if dr in('up','down'): n=aw; nb=bw
    else: n=ah; nb=bh
    return [i for i in range(n) if 0<=i-off<nb]
def band_cells(n,dr,idx,depth=D):
    """cases (x,y,d,i) de la bande de profondeur depth cote bord dr pour les indices idx"""
    w,h=dims(n);out=[]
    for i in idx:
        for d in range(depth):
            if dr=='up': out.append((i,d,d,i))
            elif dr=='down': out.append((i,h-1-d,d,i))
            elif dr=='left': out.append((d,i,d,i))
            else: out.append((w-1-d,i,d,i))
    return out
def events_in(n,cells):
    s={(x,y) for x,y,_,_ in cells};d=MAPS[n];res=[]
    for k in ('object_events','warp_events','coord_events','bg_events'):
        for e in d.get(k,[]):
            if (e['x'],e['y']) in s: res.append((k,e['x'],e['y']))
    return res
