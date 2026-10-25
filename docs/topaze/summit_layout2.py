"""Layout du sommet v2 : vraie montee (le haut du canyon de Sevault + plateforme agrandie). Sortie : map.bin + layouts.json + rendu."""
import json,struct,os,shutil,sys
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import maprender as M
S='SevenIsland_SevaultCanyon'; D=S+'_Summit'; LID='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT'
lj=json.load(open('data/layouts/layouts.json'))
src=[l for l in lj['layouts'] if l.get('id')=='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'][0]
d=open('data/layouts/%s/map.bin'%S,'rb').read(); W=src['width']
g=lambda x,y:struct.unpack_from('<H',d,(y*W+x)*2)[0]
row=lambda y:[g(x,y) for x in range(6,21)]
FACE=g(9,3); FILL=g(6,0)
def clean(r):  # retire les bouches de grotte
    return [FACE if (v&0x3ff)==0xa9 else v for v in r]
rows=[row(0),row(0),row(2),clean(row(3))]
rows+= [row(4),row(5)]*3          # plateforme : y 4..9
rows+= [clean(row(y)) for y in range(6,39)]   # montee : src 6..38 -> y 10..42
rows+= [[FILL]*15,[FILL]*15,[FILL]*15]
# bouche d'entree sous la case (10,25)
mouth=(FACE&~0x3ff&~(3<<10))|0xa9
rows.insert(43,[FILL]*15) if False else None
rows[43]=[FILL]*15; rows[43][8]=(g(14,39)&~0x3ff&~(3<<10)|0xa9)|(1<<10)
rows[43][8]=(g(14,39)&~0x3ff)|0xa9|(1<<10)
H=len(rows); print('H',H)
data=b''.join(struct.pack('<H',v) for r in rows for v in r)
os.makedirs('data/layouts/'+D,exist_ok=True); open('data/layouts/%s/map.bin'%D,'wb').write(data)
shutil.copy('data/layouts/%s/border.bin'%S,'data/layouts/%s/border.bin'%D)
for l in lj['layouts']:
    if l.get('id')==LID: l['height']=H; l['width']=15; new=l
json.dump(lj,open('data/layouts/layouts.json','w'),indent=2); open('data/layouts/layouts.json','a').write('\n')
M.render(new,'/tmp/gx/maps/summit2.png')
import collections
c=lambda x,y:(struct.unpack_from('<H',data,(y*15+x)*2)[0]>>10)&3
st=(8,42); seen={st}; q=collections.deque([st])
while q:
    a=q.popleft()
    for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
        n=(a[0]+dx,a[1]+dy)
        if 0<=n[0]<15 and 0<=n[1]<H and n not in seen and not c(*n): seen.add(n); q.append(n)
print('plateforme atteinte:',all((x,y) in seen for x in (8,) for y in (6,8)),(11,11) in seen,(12,11) in seen,(8,4) in seen)
