#!/usr/bin/env python3
"""Echo 7 finale : les 6 legendaires vivent dans une grotte verdoyante (copie de la Tanoby Key) dont la bouche s'ouvre dans la falaise nord
du plateau de Sevault (11,3). 4 gardiens (W0-W3, deplaces depuis les escaliers) couvrent les rangees ; les legendaires refusent tant qu'un gardien reste. Idempotent."""
import json,re,os,shutil,struct,sys
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import mapkit
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
S='SevenIsland_SevaultCanyon'; D=S+'_Grove'; LID='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_GROVE'; MID='MAP_SEVEN_ISLAND_SEVAULT_CANYON_GROVE'
lj=json.load(open('data/layouts/layouts.json'))
if any(l.get('id')==LID for l in lj['layouts']): print('deja'); raise SystemExit
C=['Kyogre','Groudon','Rayquaza','Latias','Latios','Jirachi']
TR=['COOLTRAINER_BROOKE','COOLTRAINER_AUSTINA','COOLTRAINER_JULIE','SUPER_NERD_2']
# layout
os.makedirs('data/layouts/'+D,exist_ok=True)
for f in ('map.bin','border.bin'): shutil.copy('data/layouts/%s_TanobyKey/%s'%(S,f),'data/layouts/%s/%s'%(D,f))
b=bytearray(open('data/layouts/%s/map.bin'%D,'rb').read()); w=15
v=struct.unpack_from('<H',b,(5*w+7)*2)[0]
for x in (6,8): struct.pack_into('<H',b,(5*w+x)*2,v)
open('data/layouts/%s/map.bin'%D,'wb').write(b)
src=[l for l in lj['layouts'] if l.get('id')=='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_TANOBY_KEY'][0]
new=dict(src); new['id']=LID; new['name']=D+'_Layout'; new['border_filepath']='data/layouts/%s/border.bin'%D; new['blockdata_filepath']='data/layouts/%s/map.bin'%D
lj['layouts'].append(new); save('data/layouts/layouts.json',lj)
# bouche dans la falaise nord du plateau
dx,dy=11,3
L=mapkit.Layout('LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'); i=dy*L.w+dx; L.g[i]=(L.g[i]&~0x3ff&~(3<<10))|0xa9; L.save()
pj=json.load(open('data/maps/%s/map.json'%S))
pj['warp_events'].append({"x":dx,"y":dy,"elevation":3,"dest_map":MID,"dest_warp_id":"0"}); pw=len(pj['warp_events'])-1
leg=[]; keep=[]
for o in pj['object_events']:
    if any(o['script']==f'{S}_EventScript_{c}' for c in C) or re.search(r'_EventScript_W\d$',o['script']): leg.append(o)
    else: keep.append(o)
pj['object_events']=keep
pj['coord_events']+=[{"type":"trigger","x":dx,"y":dy+1,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":str(v_),"script":S+"_EventScript_GroveLocked"} for v_ in range(22)]
save('data/maps/%s/map.json'%S,pj)
# carte de la grotte
tk=json.load(open('data/maps/%s_TanobyKey/map.json'%S))
mj=dict(tk); mj['id']=MID; mj['name']=D; mj['layout']=LID; mj['region_map_section']='MAPSEC_SEVAULT_CANYON'; mj['connections']=None
mj['warp_events']=[{"x":7,"y":13,"elevation":3,"dest_map":"MAP_SEVEN_ISLAND_SEVAULT_CANYON","dest_warp_id":str(pw)}]
mj['coord_events']=[]; mj['bg_events']=[]
pos={'Kyogre':(6,3),'Groudon':(8,3),'Rayquaza':(7,3),'Latias':(4,4),'Latios':(10,4),'Jirachi':(7,5)}
gp=[(5,12,'RIGHT'),(9,10,'LEFT'),(5,8,'RIGHT'),(9,6,'LEFT')]
objs=[]
for o in leg:
    o=dict(o); o['elevation']=3; o['movement_range_x']=0; o['movement_range_y']=0; o['movement_type']='MOVEMENT_TYPE_FACE_DOWN'
    m=re.search(r'_EventScript_(\w+)$',o['script']).group(1)
    if m in pos: o['x'],o['y']=pos[m]
    else:
        j=int(m[1]); o['x'],o['y'],f=gp[j]; o['movement_type']='MOVEMENT_TYPE_FACE_'+f; o['trainer_sight_or_berry_tree_id']='4'
    objs.append(o)
mj['object_events']=objs; os.makedirs('data/maps/'+D,exist_ok=True); save('data/maps/%s/map.json'%D,mj)
# scripts
scr=f"""{D}_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, {D}_OnTransition
	.byte 0

{D}_OnTransition::
	setflag FLAG_TEMP_11
	setflag FLAG_TEMP_14
	setflag FLAG_TEMP_1E
	setflag FLAG_TEMP_1F
	call_if_eq VAR_ECHO_STAGE, 22, {S}_EventScript_ShowWardens
	end
"""
wr(f'data/maps/{D}/scripts.inc',scr); wr(f'data/maps/{D}/text.inc','')
sp=f'data/maps/{S}/scripts.inc'; s=rd(sp)
for l in ('\tsetflag FLAG_TEMP_11\n','\tsetflag FLAG_TEMP_14\n','\tsetflag FLAG_TEMP_1E\n','\tsetflag FLAG_TEMP_1F\n',f'\tcall_if_eq VAR_ECHO_STAGE, 22, {S}_EventScript_ShowWardens\n'):
    assert l in s,l; s=s.replace(l,'',1)
for c in C:
    lab=f'{S}_EventScript_{c}::\n\tgoto_if_questlog EventScript_ReleaseEnd\n\tspecial QuestLog_CutRecording\n\tlock\n\tfaceplayer\n'
    assert lab in s,c
    s=s.replace(lab,lab+''.join(f'\tgoto_if_not_defeated TRAINER_{t}, {S}_EventScript_GuardsLeft\n' for t in TR),1)
s+=f"\n@ Topaze: la bouche de grotte (11,3) reste fermee avant l'Echo final\n{S}_EventScript_GroveLocked::\n\tlockall\n\tmsgbox {S}_Text_GroveLocked\n\tapplymovement LOCALID_PLAYER, {S}_Movement_GroveBack\n\twaitmovement 0\n\treleaseall\n\tend\n\n{S}_Movement_GroveBack::\n\twalk_down\n\tstep_end\n"
wr(sp,s)
tp=f'data/maps/{S}/text.inc'; t=rd(tp)
t=t.replace('"Left stair is open. Mind the top.$"','"The grove is open. Mind the top.$"').replace('"The way is open.$"','"The way is open. Go on.$"')
t+=f'\n{S}_Text_GroveLocked::\n    .string "A mossy cave mouth. The air within\\n"\n    .string "hums. It is not time yet.$"\n'
wr(tp,t)
j2=json.load(open('data/maps/map_groups.json'))
if D not in j2['gMapGroup_SpecialArea']: j2['gMapGroup_SpecialArea'].append(D)
save('data/maps/map_groups.json',j2)
f='data/event_scripts.s'; s=rd(f)
a='\t.include "data/maps/%s/scripts.inc"\n'%S; assert a in s; s=s.replace(a,a+'\t.include "data/maps/%s/scripts.inc"\n'%D,1)
a='\t.include "data/maps/%s/text.inc"\n'%S; assert a in s; s=s.replace(a,a+'\t.include "data/maps/%s/text.inc"\n'%D,1); wr(f,s)
print('ok',pw)
