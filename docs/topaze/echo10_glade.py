#!/usr/bin/env python3
"""Echo 7 : Celebi a sa propre petite grotte (Glade, copie de la Tanoby Key), bouche (15,3) ouverte des l'etape 19 ;
la grotte du finale (Grove) est reservee a la scene + legendaires : fermee avant l'etape 21. Idempotent."""
import json,os,shutil,sys
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import mapkit
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
S='SevenIsland_SevaultCanyon'; D=S+'_Glade'; LID='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_GLADE'; MID='MAP_SEVEN_ISLAND_SEVAULT_CANYON_GLADE'
lj=json.load(open('data/layouts/layouts.json'))
if any(l.get('id')==LID for l in lj['layouts']): print('deja'); raise SystemExit
os.makedirs('data/layouts/'+D,exist_ok=True)
for f in ('map.bin','border.bin'): shutil.copy('data/layouts/%s_TanobyKey/%s'%(S,f),'data/layouts/%s/%s'%(D,f))
src=[l for l in lj['layouts'] if l.get('id')=='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_TANOBY_KEY'][0]
new=dict(src); new['id']=LID; new['name']=D+'_Layout'; new['border_filepath']='data/layouts/%s/border.bin'%D; new['blockdata_filepath']='data/layouts/%s/map.bin'%D
lj['layouts'].append(new); save('data/layouts/layouts.json',lj)
dx,dy=15,3
L=mapkit.Layout('LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'); i=dy*L.w+dx; L.g[i]=(L.g[i]&~0x3ff&~(3<<10))|0xa9; L.save()
pj=json.load(open('data/maps/%s/map.json'%S))
pj['warp_events'].append({"x":dx,"y":dy,"elevation":3,"dest_map":MID,"dest_warp_id":"0"}); pw=len(pj['warp_events'])-1
pj['coord_events']+=[{"type":"trigger","x":dx,"y":dy+1,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":str(v),"script":S+"_EventScript_GladeLocked"} for v in range(19)]
save('data/maps/%s/map.json'%S,pj)
gj=json.load(open('data/maps/%s_Grove/map.json'%S))
cel=[o for o in gj['object_events'] if o['script'].endswith('_EventScript_Celebi')][0]; gj['object_events'].remove(cel)
save('data/maps/%s_Grove/map.json'%S,gj)
pj=json.load(open('data/maps/%s/map.json'%S))
pj['coord_events']+=[{"type":"trigger","x":11,"y":4,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":str(v),"script":S+"_EventScript_GroveLocked"} for v in (19,20)]
save('data/maps/%s/map.json'%S,pj)
tk=json.load(open('data/maps/%s_TanobyKey/map.json'%S))
mj=dict(tk); mj['id']=MID; mj['name']=D; mj['layout']=LID; mj['region_map_section']='MAPSEC_SEVAULT_CANYON'; mj['connections']=None
mj['warp_events']=[{"x":7,"y":13,"elevation":3,"dest_map":"MAP_SEVEN_ISLAND_SEVAULT_CANYON","dest_warp_id":str(pw)}]
mj['coord_events']=[]; mj['bg_events']=[]
cel.update(x=7,y=5); mj['object_events']=[cel]
os.makedirs('data/maps/'+D,exist_ok=True); save('data/maps/%s/map.json'%D,mj)
wr(f'data/maps/{D}/scripts.inc',f'{D}_MapScripts::\n\t.byte 0\n'); wr(f'data/maps/{D}/text.inc','')
sp=f'data/maps/{S}/scripts.inc'; s=rd(sp)
s+=f"\n@ Topaze: la petite grotte de Celebi (15,3) reste fermee avant l'Echo 7\n{S}_EventScript_GladeLocked::\n\tlockall\n\tmsgbox {S}_Text_GladeLocked\n\tapplymovement LOCALID_PLAYER, {S}_Movement_GroveBack\n\twaitmovement 0\n\treleaseall\n\tend\n"
wr(sp,s)
tp=f'data/maps/{S}/text.inc'; wr(tp,rd(tp)+f'\n{S}_Text_GladeLocked::\n    .string "A small, mossy cave mouth. Nothing\\n"\n    .string "stirs inside. Not yet.$"\n')
j2=json.load(open('data/maps/map_groups.json'))
if D not in j2['gMapGroup_SpecialArea']: j2['gMapGroup_SpecialArea'].append(D)
save('data/maps/map_groups.json',j2)
f='data/event_scripts.s'; s=rd(f)
a='\t.include "data/maps/%s/scripts.inc"\n'%S; s=s.replace(a,a+'\t.include "data/maps/%s/scripts.inc"\n'%D,1)
a='\t.include "data/maps/%s/text.inc"\n'%S; s=s.replace(a,a+'\t.include "data/maps/%s/text.inc"\n'%D,1); wr(f,s); print('ok',pw)
