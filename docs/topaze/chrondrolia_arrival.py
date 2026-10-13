#!/usr/bin/env python3
"""Route to Chrondrolia + calm arrival. Run once from repo root.
- Fuchsia south police stay (volcano closure), Route 20 sea closure (Route 19 side + SEAFOAM caves),
- Chrondrolia: calm NPCs (power plant is here because of the volcano heat; "the stone is not here"),
- Nox / PC hints point to GRENALUX -> ROUTE 21 by sea."""
import json,re,sys
if 'PoliceSouth' in open('data/maps/FuchsiaCity/scripts.inc').read():
    print('already applied'); sys.exit(0)
rd=lambda p:open(p).read()
wr=lambda p,s:open(p,'w').write(s)
def sub(p,old,new):
    s=rd(p); assert old in s,(p,old[:50]); wr(p,s.replace(old,new,1))
def mktext(label,boxes):
    out=label+'::\n'
    for bi,box in enumerate(boxes):
        for li,l in enumerate(box):
            ll=li==len(box)-1; lb=bi==len(boxes)-1
            for seg in [re.sub(r'\{[^}]*\}','X',l)]: assert len(seg)<=35,(len(seg),l)
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
def addtext(p,s): wr(p,rd(p).rstrip('\n')+'\n\n'+s)
def mj(n):
    p=f'data/maps/{n}/map.json'; return p,json.load(open(p))
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')

# ---- Fuchsia: south police stay forever (volcano) ----
p,m=mj('FuchsiaCity')
n=0
for o in m['object_events']:
    if o['script']=='FuchsiaCity_EventScript_Police' and o['y']==27:
        o['script']='FuchsiaCity_EventScript_PoliceSouth'; o['flag']='FLAG_TEMP_9'; n+=1
assert n==6; save(p,m)
sub('data/maps/FuchsiaCity/scripts.inc','FuchsiaCity_EventScript_PoliceDone::','''FuchsiaCity_EventScript_PoliceSouth::
	lock
	faceplayer
	goto_if_unset FLAG_AMETHYST_RAID_DONE, FuchsiaCity_EventScript_PoliceSouthRaid
	msgbox FuchsiaCity_Text_PoliceVolcano
	release
	end

FuchsiaCity_EventScript_PoliceSouthRaid::
	msgbox FuchsiaCity_Text_PoliceRaid
	release
	end

FuchsiaCity_EventScript_PoliceDone::''')
addtext('data/maps/FuchsiaCity/text.inc',mktext('FuchsiaCity_Text_PoliceVolcano',[
 ["The sea road south is closed."],
 ["The SEAFOAM volcano erupted and","the water is molten rock."],
 ["Looking for CHRONDROLIA? Go back","to GRENALUX and SURF south."]]))

# ---- Route 20: sea closed ----
p,m=mj('Route20')
tiles=[(w['x'],w['y'],w['elevation'],'Route20_EventScript_SeaClosed') for w in m['warp_events'] if w['dest_map']=='MAP_ROUTE19']
tiles+=[(w['x'],w['y'],w['elevation'],'Route20_EventScript_CaveClosed') for w in m['warp_events'] if w['dest_map']=='MAP_SEAFOAM_ISLANDS_1F']
assert len(tiles)==17
for x,y,e,s in tiles:
    m['coord_events'].append({"type":"trigger","x":x,"y":y,"elevation":e,"var":"VAR_TEMP_1","var_value":"0","script":s})
save(p,m)
sp='data/maps/Route20/scripts.inc'
wr(sp,rd(sp).rstrip('\n')+'''

Route20_EventScript_SeaClosed::
	lockall
	msgbox Route20_Text_SeaClosed
	closemessage
	applymovement LOCALID_PLAYER, Route20_Movement_StepLeft
	waitmovement 0
	releaseall
	end

Route20_EventScript_CaveClosed::
	lockall
	msgbox Route20_Text_CaveClosed
	closemessage
	applymovement LOCALID_PLAYER, Route20_Movement_StepDown
	waitmovement 0
	releaseall
	end

Route20_Movement_StepLeft::
	walk_left
	step_end

Route20_Movement_StepDown::
	walk_down
	step_end
''')
addtext('data/maps/Route20/text.inc',mktext('Route20_Text_SeaClosed',[
 ["COAST GUARD: Turn back!"],
 ["The SEAFOAM volcano erupted. The","sea ahead is lava and steam."],
 ["Nobody passes. Not even POKéMON."]])+'\n'+mktext('Route20_Text_CaveClosed',[
 ["A wall of heat and steam blasts","out of the cave!"],
 ["The way in is far too hot."]]))

# ---- Chrondrolia: calm arrival ----
p,m=mj('CinnabarIsland')
def obj(gfx,x,y,script,mv='MOVEMENT_TYPE_FACE_DOWN'):
    return {"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":mv,"movement_range_x":1,"movement_range_y":1,
     "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":script,"flag":"0"}
m['object_events']+=[
 obj('OBJ_EVENT_GFX_WORKER_M',6,10,'CinnabarIsland_EventScript_PlantWorker','MOVEMENT_TYPE_FACE_UP'),
 obj('OBJ_EVENT_GFX_GENTLEMAN',14,10,'CinnabarIsland_EventScript_Mayor','MOVEMENT_TYPE_FACE_LEFT'),
 obj('OBJ_EVENT_GFX_SCIENTIST',19,10,'CinnabarIsland_EventScript_Scientist','MOVEMENT_TYPE_FACE_DOWN'),
 obj('OBJ_EVENT_GFX_LITTLE_GIRL',12,15,'CinnabarIsland_EventScript_LittleGirl','MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT')]
save(p,m)
sp='data/maps/CinnabarIsland/scripts.inc'
sub(sp,'''CinnabarIsland_EventScript_OldMan::
	msgbox CinnabarIsland_Text_ScientistsExperimentInMansion, MSGBOX_NPC
	end
''','''CinnabarIsland_EventScript_OldMan::
	msgbox CinnabarIsland_Text_ScientistsExperimentInMansion, MSGBOX_NPC
	end

CinnabarIsland_EventScript_PlantWorker::
	msgbox CinnabarIsland_Text_PlantWorker, MSGBOX_NPC
	end

CinnabarIsland_EventScript_Mayor::
	msgbox CinnabarIsland_Text_Mayor, MSGBOX_NPC
	end

CinnabarIsland_EventScript_Scientist::
	msgbox CinnabarIsland_Text_Scientist, MSGBOX_NPC
	end

CinnabarIsland_EventScript_LittleGirl::
	msgbox CinnabarIsland_Text_LittleGirl, MSGBOX_NPC
	end
''')
tp='data/maps/CinnabarIsland/text.inc'; t=rd(tp)
a=t.index('CinnabarIsland_Text_ScientistsExperimentInMansion::'); b=t.index('CinnabarIsland_Text_IslandSign::')
t=t[:a]+mktext('CinnabarIsland_Text_ScientistsExperimentInMansion',[
 ["That big building is the PLANT."],
 ["They say it was a burned mansion","long ago. Now it runs on heat."],
 ["Volcano heat. Free power, forever."]])+'\n'+t[b:]
wr(tp,t)
addtext(tp,mktext('CinnabarIsland_Text_PlantWorker',[
 ["WORKER: Ever wonder why the PLANT","stands on this island?"],
 ["The SEAFOAM volcano sleeps right","under the sea. All that heat boils"],
 ["our water into steam. The steam","spins the turbines. Free power!"],
 ["Half the lights in KANTO come","from this rock."]])+'\n'+mktext('CinnabarIsland_Text_Mayor',[
 ["MAYOR: Welcome to CHRONDROLIA!"],
 ["Thieves? Stones? We heard the","rumors. None of it came here."],
 ["There is no precious stone on this","island. The TOPAZ is only a name."],
 ["Relax, trainer. Visit the GYM,","enjoy the lights."]])+'\n'+mktext('CinnabarIsland_Text_Scientist',[
 ["SCIENTIST: Ten years ago the AURA","changed every POKéMON's type."],
 ["Not our grid. Not our island.","The volcano keeps it stable."],
 ["Everything is safe here. Really."]])+'\n'+mktext('CinnabarIsland_Text_LittleGirl',[
 ["Grandma says the stone of this","town is only a fairy tale."],
 ["But the big pylon hums at night.","I like it!"]]))
# ---- Nox / PC hints ----
gt='data/maps/SaffronCity_Gym/text.inc'; s=rd(gt)
a=s.index('SaffronCity_Gym_Text_StoneGift::')
s=s[:a]+mktext('SaffronCity_Gym_Text_StoneGift',[
 ["NOX: The HEMATITE is gone. He","took it before I could hide it."],
 ["But you have the others. He needs","them all. Make him wait."],
 ["Go back to GRENALUX and SURF south","along ROUTE 21. A city of lightning"],
 ["waits there. The old road by","FUCHSIA is molten rock now."]])
wr(gt,s)
print('applied')
