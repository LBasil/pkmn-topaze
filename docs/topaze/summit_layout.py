import json,struct,os,shutil,sys
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import maprender as M
S='SevenIsland_SevaultCanyon'; D=S+'_Summit'; LID='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT'
lj=json.load(open('data/layouts/layouts.json'))
src=[l for l in lj['layouts'] if l.get('id')=='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'][0]
d=open(src['blockdata_filepath'],'rb').read(); W=src['width']
g=lambda x,y:struct.unpack_from('<H',d,(y*W+x)*2)[0]
row=lambda y:[g(x,y) for x in range(6,21)]
FILL=g(6,0)
r2,r3,r4,r5,r6,r7,r8=[row(y) for y in (2,3,4,5,6,7,8)]
r3=[(r3[5]&~0x3ff|0x079 if False else r3[4]) if (i in (5,9)) else v for i,v in enumerate(r3)]   # retire les bouches de grotte
rows=[row(0),row(0),r2,r3]+[r4,r5]*3+[r6,r7,r8]
H=len(rows)
rows=[list(r) for r in rows]
# fermer la bande de droite (x=17,18 -> index 11,12) sous la plateforme
for y in range(10,H):
    for i in (11,12): rows[y][i]=FILL
# escaliers bas (index 7,8 sur row8) -> falaise ; bouche de sortie au milieu
for i in (7,8): rows[H-1][i]=r8[3]
i=5; rows[H-1][i]=(r8[3]&~0x3ff&~(3<<10))|0xa9
data=b''.join(struct.pack('<H',v) for r in rows for v in r)
os.makedirs('data/layouts/'+D,exist_ok=True); open('data/layouts/%s/map.bin'%D,'wb').write(data)
shutil.copy('data/layouts/%s/border.bin'%S,'data/layouts/%s/border.bin'%D)
lj['layouts']=[l for l in lj['layouts'] if l.get('id')!=LID]
new=dict(src); new['id']=LID; new['name']=D+'_Layout'; new['width']=15; new['height']=H
new['border_filepath']='data/layouts/%s/border.bin'%D; new['blockdata_filepath']='data/layouts/%s/map.bin'%D
lj['layouts'].append(new); json.dump(lj,open('data/layouts/layouts.json','w'),indent=2); open('data/layouts/layouts.json','a').write('\n')
M.render(new,'/tmp/gx/maps/summit.png'); print(H)
