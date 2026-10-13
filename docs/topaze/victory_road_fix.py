#!/usr/bin/env python3
"""Correctif Route Victoire : le QG ET la scene finale sont DANS la grotte (pas a la sortie sur la Route 23).
Retire la scene 'Red attend' de la Route 23 ; scene finale dans la salle de sortie est de la 2F (declencheurs sur les 4 cases d'approche des warps de sortie) :
l'ombre du patron prend l'OPALE a Red et disparait, VESPER (3e duel) garde la salle, Red abime reste. Idempotent (marqueur dans scripts)."""
import json,re,sys
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
if 'VictoryRoad_2F_EventScript_FinalScene' in rd('data/maps/VictoryRoad_2F/scripts.inc'): print('already'); sys.exit(0)
def cut(s,start,end):
    a=s.index(start); b=s.index(end,a); return s[:a]+s[b:]
def mktext(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            assert len(l)<=35,(len(l),l)
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
# ---- Route 23 : remove end scene ----
p='data/maps/Route23/map.json'; m=json.load(open(p))
m['object_events']=[o for o in m['object_events'] if o.get('local_id')!='LOCALID_VR_RED_END']
m['coord_events']=[c for c in m['coord_events'] if c['script']!='Route23_EventScript_RedAtEnd']
json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
sp='data/maps/Route23/scripts.inc'; s=rd(sp)
a=s.index('\tgoto_if_set FLAG_VR_RED_MET, Route23_EventScript_RedCaveDone'); b=s.index('Route23_EventScript_RedStub::')
s=s[:a]+'\tgoto_if_set FLAG_VR_RED_MET, Route23_EventScript_RedCaveDone\n\tend\n\nRoute23_EventScript_RedCaveDone::\n\tsetvar VAR_TEMP_4, 1\n\tend\n\n'+s[b:]
s=cut(s,'Route23_EventScript_RedAtEnd::','\x00') if False else s
a=s.index('Route23_EventScript_RedAtEnd::'); b=s.index('step_end',s.index('Route23_Movement_RedWalkNorth::'))+len('step_end\n'); s=s[:a]+s[b:].lstrip('\n')
s=s.replace('\tsetflag FLAG_TEMP_2\n','',1)
wr(sp,s)
tp='data/maps/Route23/text.inc'; t=rd(tp)
for lab in ('RedEndA','RedEndB','RedEndC'):
    a=t.index('Route23_Text_%s::'%lab); b=t.find('\n\n',a); b=len(t) if b<0 else b; t=t[:a]+t[b:].lstrip('\n')
t=t.rstrip('\n')+'\n'
wr(tp,t)
# ---- 2F : final scene ----
p='data/maps/VictoryRoad_2F/map.json'; m=json.load(open(p))
m['object_events']=[o for o in m['object_events'] if o['script']!='VictoryRoad_2F_EventScript_Vesper']
def npc(loc,gfx,x,y,script,flag,face):
    return {"local_id":loc,"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
            "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":script,"flag":flag}
m['object_events'].append(npc('LOCALID_VR_VESPER','OBJ_EVENT_GFX_ROCKET_F',46,10,'VictoryRoad_2F_EventScript_Stub','FLAG_TEMP_1','DOWN'))
m['object_events'].append(npc('LOCALID_VR_RED_2F','OBJ_EVENT_GFX_RED_NORMAL',48,10,'VictoryRoad_2F_EventScript_RedTalk','FLAG_TEMP_2','LEFT'))
for (x,y) in ((47,12),(48,11),(49,12),(47,14)):
    m['coord_events'].append({"type":"trigger","x":x,"y":y,"elevation":3,"var":"VAR_TEMP_6","var_value":"0","script":"VictoryRoad_2F_EventScript_FinalScene"})
json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
sp='data/maps/VictoryRoad_2F/scripts.inc'; s=rd(sp)
a=s.index('VictoryRoad_2F_EventScript_Vesper::'); s=s[:a].rstrip('\n')+'\n'
s=s.replace('\tmap_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad\n','\tmap_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad\n\tmap_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_2F_OnTransition\n',1)
s+='''
VictoryRoad_2F_OnTransition::
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_FinalDone
	goto_if_unset FLAG_VR_RED_MET, VictoryRoad_2F_EventScript_NoRed
	end

VictoryRoad_2F_EventScript_FinalDone::
	setvar VAR_TEMP_6, 1
	setflag FLAG_TEMP_1
	end

VictoryRoad_2F_EventScript_NoRed::
	setvar VAR_TEMP_6, 1
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	end

VictoryRoad_2F_EventScript_Stub::
	end

VictoryRoad_2F_EventScript_RedTalk::
	lock
	faceplayer
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_RedHeal
	msgbox VictoryRoad_2F_Text_RedSilent
	release
	end

VictoryRoad_2F_EventScript_RedHeal::
	msgbox VictoryRoad_2F_Text_RedHeals
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox VictoryRoad_2F_Text_RedSilent
	release
	end

VictoryRoad_2F_EventScript_FinalScene::
	lockall
	msgbox VictoryRoad_2F_Text_ShapeA
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	playse SE_THUNDER
	special ShakeScreen
	waitstate
	msgbox VictoryRoad_2F_Text_ShapeB
	closemessage
	fadescreen FADE_TO_BLACK
	delay 40
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_2F_Text_VesperIntro
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_VR_VESPER
	trainerbattle_no_intro TRAINER_MAGMA_ADMIN_TABITHA, VictoryRoad_2F_Text_VesperDefeat
	msgbox VictoryRoad_2F_Text_VesperPost
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_VR_VESPER
	delay 20
	fadescreen FADE_FROM_BLACK
	msgbox VictoryRoad_2F_Text_RedAfter
	closemessage
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_6, 1
	releaseall
	end
'''
wr(sp,s)
tp='data/maps/VictoryRoad_2F/text.inc'; t=rd(tp)
for lab in ('VesperIntro','VesperDefeat','VesperPost'):
    a=t.index('VictoryRoad_2F_Text_%s::'%lab); b=t.find('\n\n',a); b=len(t) if b<0 else b; t=t[:a]+t[b:].lstrip('\n')
t=t.rstrip('\n')+'\n\n'
t+=mktext('VictoryRoad_2F_Text_ShapeA',[["The exit chamber is freezing.","RED kneels, the BLACK OPAL held"],["out in both hands. Above him","stands a shape made of darkness."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_ShapeB',[["It reaches out. The BLACK OPAL","goes dark in RED's palms, then"],["dissolves into the shape. The ten","stones are one now."],["The shape turns its head toward","you. Then the cave goes black."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_VesperIntro',[["VESPER: Third time, child.","The MASTER has what he came for."],["I stay to see that you do not","follow him. Even now."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_VesperDefeat',[["…Again. Again you break the","pattern."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_VesperPost',[["VESPER: Go, then. The stones are","gathered. What comes next is not"],["for us. The LEAGUE needs a","witness, not a hero."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_RedAfter',[["RED lowers his head. He did not","win. Nobody could."],["He looks at you, and nods once."]])+'\n'
t+=mktext('VictoryRoad_2F_Text_RedSilent',[["RED: ……"]])+'\n'
t+=mktext('VictoryRoad_2F_Text_RedHeals',[["RED takes out a thermos and lets","your POKéMON drink. They feel","fine again."]])
wr(tp,t)
print('ok')
