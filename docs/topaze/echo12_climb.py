#!/usr/bin/env python3
"""Echo 7 v3 : Celebi retourne dans la grotte du milieu (11,3) ; le sommet (bouche (17,3)) est une vraie montee ; la grotte des legendaires s'ouvre au fond de la plateforme du sommet (8,3).
Retire la bouche (15,3). Suppose summit_layout2.py lance. Idempotent (marqueur : warp Grove dans Summit)."""
import json,os,sys,re
sys.path[:0]=['docs/topaze','tools/topaze/maps']
import mapkit
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
S='SevenIsland_SevaultCanyon'; SM=f'data/maps/{S}/map.json'; SU=f'data/maps/{S}_Summit/map.json'
su=json.load(open(SU))
if len(su['warp_events'])>1: print('deja'); raise SystemExit
sv=json.load(open(SM))
# --- Sevault : (11,3) -> Glade (Celebi) ; (15,3) retiree ; sommet devient warp 3
w=sv['warp_events']; assert (w[2]['x'],w[3]['x'],w[4]['x'])==(11,15,17)
w[2]['dest_map']='MAP_SEVEN_ISLAND_SEVAULT_CANYON_GLADE'; del w[3]
L=mapkit.Layout('LAYOUT_SEVEN_ISLAND_SEVAULT_CANYON'); L.g[3*L.w+15]=L.g[3*L.w+14]; L.save()
sv['coord_events']=[c for c in sv['coord_events'] if not c['script'].endswith(('GladeLocked','GroveHint')) and not(c['script'].endswith('GroveLocked') and int(c['var_value'])>18)]
for c in sv['coord_events']:
    if c['script'].endswith('GroveLocked'): c['script']=S+'_EventScript_CelebiCaveLocked'
save(SM,sv)
gl=json.load(open(f'data/maps/{S}_Glade/map.json')); gl['warp_events'][0]['dest_warp_id']='2'; save(f'data/maps/{S}_Glade/map.json',gl)
# --- Summit
su['warp_events']=[{"x":10,"y":26,"elevation":3,"dest_map":"MAP_SEVEN_ISLAND_SEVAULT_CANYON","dest_warp_id":"3"},
                   {"x":8,"y":3,"elevation":3,"dest_map":"MAP_SEVEN_ISLAND_SEVAULT_CANYON_GROVE","dest_warp_id":"0"}]
su['coord_events']=[{"type":"trigger","x":11,"y":11,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":"21","script":S+"_EventScript_EchoScene"},
                    {"type":"trigger","x":12,"y":11,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":"21","script":S+"_EventScript_EchoSceneB"}]
su['coord_events']+=[{"type":"trigger","x":8,"y":4,"elevation":3,"var":"VAR_ECHO_STAGE","var_value":str(v),"script":S+"_EventScript_SummitPassLocked"} for v in range(22)]
pos={'LOCALID_ECHO_SILVER':(9,6,'LEFT'),'LOCALID_ECHO_GIOVANNI':(7,6,'RIGHT'),'LOCALID_ECHO_RED':(8,5,'DOWN')}
for o in su['object_events']:
    x,y,f=pos[o['local_id']]; o.update(x=x,y=y,movement_type='MOVEMENT_TYPE_FACE_'+f)
save(SU,su)
# mouth (8,3) dans la falaise nord de la plateforme
import struct
p=f'data/layouts/{S}_Summit/map.bin'; b=bytearray(rd.__call__ if False else open(p,'rb').read())
v=struct.unpack_from('<H',b,(3*15+7)*2)[0]; struct.pack_into('<H',b,(3*15+8)*2,(v&~0x3ff&~(3<<10))|0xa9); open(p,'wb').write(b)
# --- Grove : retour vers le sommet (warp 1)
gv=json.load(open(f'data/maps/{S}_Grove/map.json')); gv['warp_events'][0].update(dest_map='MAP_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT',dest_warp_id='1'); save(f'data/maps/{S}_Grove/map.json',gv)
# --- scripts
sp=f'data/maps/{S}/scripts.inc'; s=rd(sp)
a=s.index(f'{S}_Movement_PlayerToScene::'); e=s.index('step_end',a)+9
s=s[:a]+f'{S}_Movement_PlayerToScene::\n'+'\twalk_up\n'*3+'\twalk_left\n'*3+'\tstep_end\n\n'+f'{S}_Movement_PlayerToSceneB::\n'+'\twalk_up\n'*3+'\twalk_left\n'*4+'\tstep_end\n'+s[e:]
head=f'{S}_EventScript_EchoScene::\n\tlockall\n\tclearflag FLAG_HIDE_ECHO_SCENE\n\taddobject LOCALID_ECHO_SILVER\n\taddobject LOCALID_ECHO_GIOVANNI\n\taddobject LOCALID_ECHO_RED\n\tapplymovement LOCALID_PLAYER, {S}_Movement_PlayerToScene\n\twaitmovement 0\n'
assert head in s
new=head+f'\tgoto {S}_EventScript_EchoSceneCont\n\n{S}_EventScript_EchoSceneB::\n\tlockall\n\tclearflag FLAG_HIDE_ECHO_SCENE\n\taddobject LOCALID_ECHO_SILVER\n\taddobject LOCALID_ECHO_GIOVANNI\n\taddobject LOCALID_ECHO_RED\n\tapplymovement LOCALID_PLAYER, {S}_Movement_PlayerToSceneB\n\twaitmovement 0\n\tgoto {S}_EventScript_EchoSceneCont\n\n{S}_EventScript_EchoSceneCont::\n'
s=s.replace(head,new,1)
old='\twarp MAP_SEVEN_ISLAND_SEVAULT_CANYON, 0, 11, 4\n'; assert old in s
s=s.replace(old,'\twarp MAP_SEVEN_ISLAND_SEVAULT_CANYON_SUMMIT, 0, 8, 6\n',1)
s=s.replace(f'{S}_EventScript_GroveLocked::',f'{S}_EventScript_CelebiCaveLocked::',1)
s=s.replace(f'{S}_EventScript_GroveHint::',f'{S}_EventScript_SummitPassLocked_unused::',1)
s+=f"\n{S}_EventScript_SummitPassLocked::\n\tlockall\n\tmsgbox {S}_Text_SummitPassLocked\n\tapplymovement LOCALID_PLAYER, {S}_Movement_GroveBack\n\twaitmovement 0\n\treleaseall\n\tend\n"
wr(sp,s)
tp=f'data/maps/{S}/text.inc'; t=rd(tp)
t=t.replace('"A mossy cave mouth. The air within\\n"\n    .string "hums. It is not time yet.$"','"A mossy cave mouth. Something small\\n"\n    .string "stirs within. Not yet.$"')
t=t.replace('"The sky falls silent. Far below,\\n"\n    .string "the GROVE has opened its mouth.$"','"The sky falls silent. Behind the\\n"\n    .string "peak, a dark passage has opened.$"')
t+=f'\n{S}_Text_SummitPassLocked::\n    .string "A dark passage in the rock. The\\n"\n    .string "air within hums. Not yet.$"\n'
wr(tp,t)
c='data/scripts/echo_compass.inc'; t=rd(c); wr(c,t.replace('SEVAULT CANYON, high on the cliffs.','SEVAULT CANYON, up to the summit.')); print('ok')
