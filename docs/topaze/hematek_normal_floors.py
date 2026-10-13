#!/usr/bin/env python3
"""HEMATEK tower (ex-Silph Co.): normal floors. Remove teleport pads and card-key doors.
Run once from repo root (git checkout data/maps/SilphCo_* data/layouts/SilphCo_* to redo)."""
import json,re,struct,collections
def fnum(n):
    m=re.match(r'MAP_SILPH_CO_(\d+)F$',n); return int(m.group(1)) if m else None
newidx={}; pads={}
maps={}
for f in range(2,12):
    p=f'data/maps/SilphCo_{f}F/map.json'; m=json.load(open(p)); maps[f]=(p,m)
    keep=[];rm=[];mp={}
    for i,w in enumerate(m['warp_events']):
        d=fnum(w['dest_map'])
        tele = d is not None and abs(d-f)!=1
        if tele: rm.append(w)
        else: mp[i]=len(keep); keep.append(w)
    newidx[f]=mp; pads[f]=[(w['x'],w['y']) for w in rm]; m['warp_events']=keep
for f,(p,m) in maps.items():
    for w in m['warp_events']:
        d=fnum(w['dest_map'])
        if d and d in newidx: w['dest_warp_id']=str(newidx[d][int(w['dest_warp_id'])])
    json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
    # doors
    sp=f'data/maps/SilphCo_{f}F/scripts.inc'; s=open(sp).read()
    s=re.sub(r'\tcall_if_unset FLAG_SILPH_\dF_DOOR_\d, EventScript_Close\dFDoor\d\n','',s)
    open(sp,'w').write(s)
    # pad visuals
    bp=f'data/layouts/SilphCo_{f}F/map.bin'; b=bytearray(open(bp,'rb').read())
    L=[e for e in json.load(open('data/layouts/layouts.json'))['layouts'] if e.get('id')==f'LAYOUT_SILPH_CO_{f}F'][0]
    W,H=L['width'],L['height']
    def get(x,y): return struct.unpack_from('<H',b,(y*W+x)*2)[0]
    for x,y in pads[f]:
        v=get(x,y); c=collections.Counter()
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            if 0<=x+dx<W and 0<=y+dy<H:
                n=get(x+dx,y+dy)
                if n!=v and (n&0xfc00)==(v&0xfc00): c[n]+=1
        if c:
            struct.pack_into('<H',b,(y*W+x)*2,c.most_common(1)[0][0]&0xffff|(0))
        print(f,(x,y),hex(v),'->',hex(get(x,y)))
    open(bp,'wb').write(b)
