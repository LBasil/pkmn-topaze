import json,sys,os,struct
sys.path.insert(0,os.path.dirname(__file__))
from centrale_lib import *
from collections import deque
def load(n):
    d=open(os.path.join(ROOT,'data/layouts/PokemonMansion_%s/map.bin'%n),'rb').read(); return struct.unpack('<%dH'%(len(d)//2),d)
dims={'1F':(34,26),'2F':(22,14),'3F':(26,18),'B1F':(28,20)}
for n,(w,h) in dims.items():
    g=load(n); m=json.load(open(os.path.join(ROOT,'data/maps/PokemonMansion_%s/map.json'%n)))
    free=lambda x,y:0<=x<w and 0<=y<h and not (g[y*w+x]>>10)&3
    objs={(o['x'],o['y']):o for o in m['object_events']}
    print('==',n)
    for (x,y),o in objs.items():
        if not free(x,y): print(' OBJ SUR MUR',x,y,o['script'][-24:])
    for b in m['bg_events']:
        if b['type']=='sign' and free(b['x'],b['y']): print(' sign sur sol',b['x'],b['y'])
    for wp in m['warp_events']:
        if not free(wp['x'],wp['y']): print(' WARP SUR MUR',wp['x'],wp['y'])
    st=m['warp_events'][0]; sx,sy=st['x'],st['y']
    if n=='1F': sx,sy=16,24
    seen={(sx,sy)}; q=deque([(sx,sy)])
    while q:
        x,y=q.popleft()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            a,b=x+dx,y+dy
            if (a,b) in seen or not free(a,b): continue
            if (a,b) in objs and objs[(a,b)]['trainer_type']!='TRAINER_TYPE_NONE' and False: continue
            seen.add((a,b)); q.append((a,b))
    for (x,y),o in objs.items():
        if free(x,y):
            adj=any((x+dx,y+dy) in seen for dx,dy in((1,0),(-1,0),(0,1),(0,-1))) or (x,y) in seen
            if not adj: print(' INACCESSIBLE',x,y,o['script'][-24:])
    for b in m['bg_events']:
        x,y=b['x'],b['y']
        if not any((x+dx,y+dy) in seen for dx,dy in((1,0),(-1,0),(0,1),(0,-1),(0,0))): print(' bg inaccessible',x,y,b['type'])
    for wp in m['warp_events']:
        if (wp['x'],wp['y']) not in seen: print(' warp inaccessible',wp['x'],wp['y'])
    print(' libres atteignables',len(seen))
