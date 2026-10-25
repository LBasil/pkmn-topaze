#!/usr/bin/env python3
"""Echo 7 : la scene Silver/Giovanni/Red se joue sur un sommet (map Summit, brume, cris des legendaires), bouche (17,3) du plateau, ouverte des l'etape 21.
La grotte Grove (legendaires) reste fermee jusqu'a l'etape 22. Idempotent. Suppose docs/topaze/summit_layout.py deja lance (layout)."""
import json,os,sys,re
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import mapkit
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
S='SevenIsland_SevaultCanyon'; D=S+'_Summit'; LID='LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT'; MID='MAP_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT'
if os.path.exists(f'data/maps/{D}/map.json'): print('deja'); raise SystemExit
dx,dy=17,3
L=mapkit.Layout('LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'); i=dy*L.w+dx; L.g[i]=(L.g[i]&~0x3ff&~(3<<10))|0xa9; L.save()
pj=json.load(open(f'data/maps/{S}/map.json'))
pj['warp_events'].append({"x":dx,"y":dy,"elevation":3,"dest_map":MID,"dest_warp_id":"0"}); pw=len(pj['warp_events'])-1
sc=[o for o in pj['object_events'] if o['flag']=='FLAG_HIDE_ECHO_SCENE']
pj['coord_events']+=[{"type":"trigger","x":dx,"y":dy+1,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":str(v),"script":S+"_EventScript_SummitLocked"} for v in range(21)]
pj['coord_events']+=[{"type":"trigger","x":11,"y":4,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":"21","script":S+"_EventScript_GroveLocked"}]
save(f'data/maps/{S}/map.json',pj)
gj=json.load(open(f'data/maps/{S}_Grove/map.json'))
sc=[o for o in gj['object_events'] if o.get('flag')=='FLAG_HIDE_ECHO_SCENE']
gj['object_events']=[o for o in gj['object_events'] if o.get('flag')!='FLAG_HIDE_ECHO_SCENE']
gj['coord_events']=[c for c in gj['coord_events'] if not c['script'].endswith('EchoScene')]
save(f'data/maps/{S}_Grove/map.json',gj)
pos={'LOCALID_ECHO_SILVER':(9,6,'LEFT'),'LOCALID_ECHO_GIOVANNI':(7,6,'RIGHT'),'LOCALID_ECHO_RED':(8,4,'DOWN')}
for o in sc:
    x,y,f=pos[o['local_id']]; o.update(x=x,y=y,movement_type='MOVEMENT_TYPE_FACE_'+f)
sm=json.load(open(f'data/maps/{S}/map.json'))
mj={k:sm[k] for k in sm if k not in('object_events','warp_events','coord_events','bg_events','connections')}
mj.update(id=MID,name=D,layout=LID,weather='WEATHER_FOG_HORIZONTAL',connections=None,music='MUS_SEVII_ROUTE',
  warp_events=[{"x":5,"y":12,"elevation":3,"dest_map":"MAP_SEVEN_ISLAND_SEVAULT_CANYON","dest_warp_id":str(pw)}],
  coord_events=[{"type":"trigger","x":5,"y":11,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":"21","script":S+"_EventScript_EchoScene"}],
  bg_events=[],object_events=sc)
os.makedirs('data/maps/'+D,exist_ok=True); save(f'data/maps/{D}/map.json',mj)
wr(f'data/maps/{D}/scripts.inc',f'{D}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {D}_OnTransition\n\t.byte 0\n\n{D}_OnTransition::\n\tsetflag FLAG_HIDE_ECHO_SCENE\n\tend\n'); wr(f'data/maps/{D}/text.inc','')
sp=f'data/maps/{S}/scripts.inc'; s=rd(sp)
a=s.index(f'{S}_Movement_PlayerToScene::'); b=s.index('step_end',a)+9
s=s[:a]+f'{S}_Movement_PlayerToScene::\n\twalk_left\n\twalk_left\n\twalk_up\n\twalk_up\n\twalk_up\n'+'\twalk_right\n'*5+'\tstep_end\n'+s[b:]
old=f'\tapplymovement LOCALID_PLAYER, {S}_Movement_PlayerToScene\n\twaitmovement 0\n'; assert old in s
cries=''.join(f'\tplaymoncry SPECIES_{c}, CRY_MODE_ENCOUNTER\n\twaitmoncry\n\tdelay 20\n' for c in ('KYOGRE','GROUDON','RAYQUAZA','LATIAS','LATIOS','JIRACHI'))
s=s.replace(old,old+'\tdelay 30\n'+cries+'\tdelay 40\n',1)
old=f'\twarp MAP_SEVEN_ISLAND_SEVAULT_CANYON_GROVE, 0, 7, 12\n\twaitstate\n\tend\n'; assert old in s
s=s.replace(old,f'\tmsgbox {S}_Text_SceneEnd\n\twarp MAP_SEVEN_ISLAND_SEVAULT_CANYON, 0, 11, 4\n\twaitstate\n\tend\n')
s+=f"\n@ Topaze: la bouche du sommet (17,3) reste fermee avant l'etape 21\n{S}_EventScript_SummitLocked::\n\tlockall\n\tmsgbox {S}_Text_SummitLocked\n\tapplymovement LOCALID_PLAYER, {S}_Movement_GroveBack\n\twaitmovement 0\n\treleaseall\n\tend\n"
wr(sp,s)
tp=f'data/maps/{S}/text.inc'
wr(tp,rd(tp)+f'\n{S}_Text_SummitLocked::\n    .string "A dark passage climbs into the\\n"\n    .string "clouds. The ECHO is still silent.$"\n\n{S}_Text_SceneEnd::\n    .string "The sky falls silent. Far below,\\n"\n    .string "the GROVE has opened its mouth.$"\n')
j2=json.load(open('data/maps/map_groups.json'))
if D not in j2['gMapGroup_SpecialArea']: j2['gMapGroup_SpecialArea'].append(D)
save('data/maps/map_groups.json',j2)
f='data/event_scripts.s'; s=rd(f)
a='\t.include "data/maps/%s/scripts.inc"\n'%S; s=s.replace(a,a+'\t.include "data/maps/%s/scripts.inc"\n'%D,1)
a='\t.include "data/maps/%s/text.inc"\n'%S; s=s.replace(a,a+'\t.include "data/maps/%s/text.inc"\n'%D,1); wr(f,s); print('ok',pw)
