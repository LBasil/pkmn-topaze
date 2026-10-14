# Viridian <-> Route 2 smooth connection (no warp). NOT re-runnable (git checkout data first).
# Viridian gets 4 new rows on top (primary forest band, gap x20-21); everything in Viridian shifts +4 in y.
# Route 2 bottom rows 52-55 stay primary-only (Dusk/Opal/Gradient share the same 512 base metatiles+tiles).
import json, struct, glob
R='/home/claude/pkmn-topaze/'; SH=4
def jr(p): return json.load(open(R+p))
def jw(p,j): open(R+p,'w').write(json.dumps(j,indent=2)+'\n')
def rdbin(p,w):
    b=open(R+p,'rb').read(); v=struct.unpack('<%dH'%(len(b)//2),b); return [list(v[i:i+w]) for i in range(0,len(v),w)]
def wrbin(p,rows):
    f=[t for r in rows for t in r]; open(R+p,'wb').write(struct.pack('<%dH'%len(f),*f))
vir=rdbin('data/layouts/ViridianCity/map.bin',42)
r1=rdbin('data/layouts/Route1/map.bin',26)
grass=next(t for row in r1[30:] for t in row if (t&0x3ff)==1 and ((t>>10)&3)==0)
assert (vir[0][12]&0x3ff)==0x1d4 and (vir[1][13]&0x3ff)==0x1dd
GAP=(20,21)
new=[]
for y in range(SH):
    new.append([vir[y%2][x] for x in range(42)])
for x in GAP: vir[0][x]=grass     # old row 0 gap: primary only (visible from Route 2)
wrbin('data/layouts/ViridianCity/map.bin',new+vir)
s=open(R+'data/layouts/layouts.json').read()
i=s.index('"id": "LAYOUT_VIRIDIAN_CITY"'); j=s.index('"height": 40',i)
open(R+'data/layouts/layouts.json','w').write(s[:j]+'"height": %d'%(40+SH)+s[j+len('"height": 40'):])
# Route 2 bottom: replace secondary metatiles in rows 52..55 by ground
r2=rdbin('data/layouts/Route2/map.bin',26)
gr2=r2[52][9]; assert (gr2&0x3ff)==1
for y in range(52,56):
    for x in range(26):
        if (r2[y][x]&0x3ff)>=0x200: r2[y][x]=gr2
wrbin('data/layouts/Route2/map.bin',r2)
# Viridian map.json
v=jr('data/maps/ViridianCity/map.json')
for k in ('object_events','coord_events','bg_events','warp_events'):
    for e in v.get(k,[]): e['y']+=SH
assert [w['dest_map'] for w in v['warp_events'][6:8]]==['MAP_ROUTE2']*2
v['warp_events']=v['warp_events'][:6]+v['warp_events'][8:]
v['connections']=(v['connections'] or [])+[{'map':'MAP_ROUTE2','offset':8,'direction':'up'}]
jw('data/maps/ViridianCity/map.json',v)
m=jr('data/maps/Route2/map.json')
m['warp_events']=[w for w in m['warp_events'] if w['dest_map']!='MAP_VIRIDIAN_CITY']
m['connections']=(m.get('connections') or [])+[{'map':'MAP_VIRIDIAN_CITY','offset':-8,'direction':'down'}]
jw('data/maps/Route2/map.json',m)
for f in glob.glob(R+'data/maps/*/map.json'):
    j=json.load(open(f)); ch=False
    for w in j.get('warp_events',[]):
        if w['dest_map']=='MAP_VIRIDIAN_CITY' and int(w['dest_warp_id'])>=8: w['dest_warp_id']=str(int(w['dest_warp_id'])-2); ch=True
    if ch: jw(f[len(R):],j)
h=open(R+'src/data/heal_locations.json').read()
k=h.index('"HEAL_LOCATION_VIRIDIAN_CITY"'); a=h.index('"y": 21',k)
open(R+'src/data/heal_locations.json','w').write(h[:a]+'"y": %d'%(21+SH)+h[a+len('"y": 21'):])
