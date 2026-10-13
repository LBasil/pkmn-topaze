#!/usr/bin/env python3
"""Chrondrolia stage 1: after EDDIE's badge the town blacks out; the MAYOR is an ONYBRIS mole;
4 grunts + SELENE (2nd fight) hold the PLANT; the player wins the TOPAZ; Route 19 / SEAFOAM reopen.
Run once from repo root (marker: FLAG_CHRONDROLIA_RAID_STARTED)."""
import json,re,sys
if 'FLAG_CHRONDROLIA_RAID_STARTED' in open('include/constants/flags.h').read():
    print('already applied'); sys.exit(0)
rd=lambda p:open(p).read()
wr=lambda p,s:open(p,'w').write(s)
def sub(p,old,new):
    s=rd(p); assert old in s,(p,old[:60]); wr(p,s.replace(old,new,1))
def mktext(label,boxes):
    out=label+'::\n'
    for bi,box in enumerate(boxes):
        for li,l in enumerate(box):
            ll=li==len(box)-1; lb=bi==len(boxes)-1
            assert len(re.sub(r'\{[^}]*\}','X',l))<=35,(len(l),l)
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
def addtext(p,s): wr(p,rd(p).rstrip('\n')+'\n\n'+s)
def mj(n):
    p=f'data/maps/{n}/map.json'; return p,json.load(open(p))
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')

# ---- flags ----
f='include/constants/flags.h'
sub(f,'#define FLAG_0x0B2               0x0B2','#define FLAG_CHRONDROLIA_RAID_STARTED 0x0B2')
sub(f,'#define FLAG_0x0B3               0x0B3','#define FLAG_CHRONDROLIA_RAID_DONE    0x0B3')

# ---- trainers ----
IDS={'TRAINER_RS_PSYCHIC_M':('ROCKET_GRUNT_M','GRUNT',[('GOLBAT',42),('WEEZING',43),('ARBOK',43)]),
     'TRAINER_RS_HIKER':('ROCKET_GRUNT_M','GRUNT',[('MUK',43),('ALAKAZAM',42),('RAICHU',43)]),
     'TRAINER_RS_PSYCHIC_F':('ROCKET_GRUNT_F','GRUNT',[('VENOMOTH',43),('TENTACRUEL',43),('HYPNO',42)]),
     'TRAINER_RS_LASS':('ROCKET_GRUNT_F','GRUNT',[('GOLBAT',42),('MAGNETON',43),('WEEZING',44)]),
     'TRAINER_AQUA_ADMIN_SHELLY':('MAGMA_ADMIN_F','SELENE',[('HYPNO',45),('MUK',46),('VENOMOTH',46),('TENTACRUEL',47),('GENGAR',48)])}
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
for tid,(pic,name,team) in IDS.items():
    b=re.search(r'\[%s\] = \{.*?\n    \},'%tid,tr,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_TEAM_ROCKET',b)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%pic,nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    if name=='SELENE': nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT',nb)
    sym=re.search(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    tr=tr.replace(b,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    iv=60 if name=='SELENE' else 30
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(iv,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)

# ---- plant maps ----
def trainer_obj(gfx,x,y,d,sight,script,flag,local=None):
    o={"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+d,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":str(sight),"script":script,"flag":flag}
    if local: o={"local_id":local,**o}
    return o
G=[('PokemonMansion_1F','TRAINER_RS_PSYCHIC_M','OBJ_EVENT_GFX_ROCKET_M',14,13,'DOWN',4,'1',
    ["The PLANT is ours now, kid!"],["Zzzapped…"],["SELENE is at the transformers.","Go and get crushed!"]),
   ('PokemonMansion_1F','TRAINER_RS_PSYCHIC_F','OBJ_EVENT_GFX_ROCKET_F',24,17,'LEFT',4,'2',
    ["No visitors in the turbine hall!"],["Overloaded…"],["The MAYOR opened every door for","us. Smart man."]),
   ('PokemonMansion_2F','TRAINER_RS_HIKER','OBJ_EVENT_GFX_ROCKET_M',11,9,'DOWN',3,'3',
    ["The control room is off limits!"],["Short circuit!"],["We cut the lights. You fetched the","key. Thanks for that!"]),
   ('PokemonMansion_3F','TRAINER_RS_LASS','OBJ_EVENT_GFX_ROCKET_F',14,14,'UP',3,'4',
    ["Last stop, kid! Hold it there!"],["I should have gone fishing…"],["The TOPAZ is on the pedestal.","SELENE guards it. Good luck."])]
texts={}
for mp in ('PokemonMansion_1F','PokemonMansion_2F','PokemonMansion_3F'):
    p,m=mj(mp)
    for g in G:
        if g[0]!=mp: continue
        _,tid,gfx,x,y,d,sight,lab,intro,defeat,post=g
        script=f'{mp}_EventScript_Onybris{lab}'
        m['object_events'].append(trainer_obj(gfx,x,y,d,sight,script,'FLAG_TEMP_4'))
    if mp=='PokemonMansion_3F':
        m['object_events'].append(trainer_obj('OBJ_EVENT_GFX_ROCKET_F',23,6,'DOWN',4,'PokemonMansion_3F_EventScript_OnybrisSelene','FLAG_TEMP_5','LOCALID_PLANT_SELENE'))
        m['object_events'].append({"local_id":"LOCALID_PLANT_TOPAZ","type":"object","graphics_id":"OBJ_EVENT_GFX_ITEM_BALL","x":23,"y":3,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,"trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":"PokemonMansion_3F_EventScript_Topaz","flag":"FLAG_TEMP_6"})
    save(p,m)
    sp=f'data/maps/{mp}/scripts.inc'; s=rd(sp)
    hide=f'''
{mp}_EventScript_HideOnybris::
	setflag FLAG_TEMP_4
	setflag FLAG_TEMP_5
	setflag FLAG_TEMP_6
	return
'''
    chk=f'''	goto_if_unset FLAG_CHRONDROLIA_RAID_STARTED, {mp}_EventScript_HideOnybrisEnd
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, {mp}_EventScript_HideOnybrisEnd
'''
    if 'MAP_SCRIPT_ON_TRANSITION' in s:
        s=s.replace('\tsetworldmapflag FLAG_WORLD_MAP_POWER_PLANT\n\tend\n','\tsetworldmapflag FLAG_WORLD_MAP_POWER_PLANT\n\tcall %s_EventScript_CheckOnybris\n\tend\n'%mp,1)
    else:
        s=s.replace('\t.byte 0\n','\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition\n\t.byte 0\n\n%s_OnTransition::\n\tcall %s_EventScript_CheckOnybris\n\tend\n'%(mp,mp,mp),1)
    s+=f'''
{mp}_EventScript_CheckOnybris::
	goto_if_unset FLAG_CHRONDROLIA_RAID_STARTED, {mp}_EventScript_HideOnybris
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, {mp}_EventScript_HideOnybris
	return
{hide}'''
    for g in G:
        if g[0]!=mp: continue
        _,tid,gfx,x,y,d,sight,lab,intro,defeat,post=g
        s+=f'''
{mp}_EventScript_Onybris{lab}::
	trainerbattle_single {tid}, {mp}_Text_Onybris{lab}Intro, {mp}_Text_Onybris{lab}Defeat
	msgbox {mp}_Text_Onybris{lab}Post, MSGBOX_AUTOCLOSE
	end
'''
        tx=mktext(f'{mp}_Text_Onybris{lab}Intro',[intro])+'\n'+mktext(f'{mp}_Text_Onybris{lab}Defeat',[defeat])+'\n'+mktext(f'{mp}_Text_Onybris{lab}Post',[post])
        addtext(f'data/maps/{mp}/text.inc',tx)
    wr(sp,s)
# 3F: Selene + pedestal
sp='data/maps/PokemonMansion_3F/scripts.inc'; s=rd(sp)
# simpler hide-on-defeat: SELENE hidden at transition if defeated
s=s.replace('PokemonMansion_3F_EventScript_CheckOnybris::\n','PokemonMansion_3F_EventScript_CheckOnybris::\n\tcall_if_defeated TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_EventScript_HideSelene\n',1)
s+='''
PokemonMansion_3F_EventScript_HideSelene::
	setflag FLAG_TEMP_5
	return

PokemonMansion_3F_EventScript_OnybrisSelene::
	trainerbattle_single TRAINER_AQUA_ADMIN_SHELLY, PokemonMansion_3F_Text_SeleneIntro, PokemonMansion_3F_Text_SeleneDefeat, PokemonMansion_3F_EventScript_SeleneLeaves
	end

PokemonMansion_3F_EventScript_SeleneLeaves::
	msgbox PokemonMansion_3F_Text_SelenePost
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_PLANT_SELENE
	delay 20
	fadescreen FADE_FROM_BLACK
	release
	end

PokemonMansion_3F_EventScript_Topaz::
	lockall
	msgbox PokemonMansion_3F_Text_TopazPedestal
	playfanfare MUS_OBTAIN_KEY_ITEM
	message PokemonMansion_3F_Text_ObtainedTopaz
	waitmessage
	waitfanfare
	removeobject LOCALID_PLANT_TOPAZ
	setflag FLAG_CHRONDROLIA_RAID_DONE
	releaseall
	end
'''
wr(sp,s)
addtext('data/maps/PokemonMansion_3F/text.inc',
 mktext('PokemonMansion_3F_Text_SeleneIntro',[
 ["SELENE: You again. Third time now."],
 ["The MASTER wants this TOPAZ. Its","heat will wake the SEAFOAM volcano."],
 ["Stand aside, or burn with it!"]])+'\n'+
 mktext('PokemonMansion_3F_Text_SeleneDefeat',[["SELENE: Tch… Stubborn brat."]])+'\n'+
 mktext('PokemonMansion_3F_Text_SelenePost',[
 ["SELENE: Keep your pretty rock."],
 ["The eruption on the sea road? Our","doing. The sea is a wall for you."],
 ["The MASTER waits inside the","volcano. Come, if you dare."]])+'\n'+
 mktext('PokemonMansion_3F_Text_TopazPedestal',[["A golden crystal hums on the","pedestal. The real TOPAZ!"]])+'\n'+
 mktext('PokemonMansion_3F_Text_ObtainedTopaz',[["{PLAYER} obtained the TOPAZ!"]]))

# ---- Chrondrolia: blackout scene ----
p,m=mj('CinnabarIsland')
for o in m['object_events']:
    if o['script']=='CinnabarIsland_EventScript_Mayor': o['flag']='FLAG_TEMP_5'; o['graphics_id']='OBJ_EVENT_GFX_GENTLEMAN'; o['local_id']='LOCALID_CHRONDROLIA_MAYOR'
save(p,m)
sp='data/maps/CinnabarIsland/scripts.inc'
sub(sp,'	call CinnabarIsland_EventScript_CheckUnlockGym\n','''	call CinnabarIsland_EventScript_CheckUnlockGym
	call_if_set FLAG_CHRONDROLIA_RAID_STARTED, CinnabarIsland_EventScript_HideMayor
	call_if_set FLAG_BADGE07_GET, CinnabarIsland_EventScript_CheckBlackout
''')
sub(sp,'	map_script_2 VAR_MAP_SCENE_CINNABAR_ISLAND_2, 1, CinnabarIsland_EventScript_ExitPokeCenterForOneIsland\n','	map_script_2 VAR_TEMP_2, 1, CinnabarIsland_EventScript_BlackoutScene\n	map_script_2 VAR_MAP_SCENE_CINNABAR_ISLAND_2, 1, CinnabarIsland_EventScript_ExitPokeCenterForOneIsland\n')
sub(sp,'CinnabarIsland_EventScript_PlantWorker::','''CinnabarIsland_EventScript_HideMayor::
	setflag FLAG_TEMP_5
	return

CinnabarIsland_EventScript_CheckBlackout::
	goto_if_set FLAG_CHRONDROLIA_RAID_STARTED, CinnabarIsland_EventScript_CheckBlackoutEnd
	setvar VAR_TEMP_2, 1
CinnabarIsland_EventScript_CheckBlackoutEnd::
	return

CinnabarIsland_Movement_MayorComes::
	walk_right
	walk_right
	walk_right
	walk_right
	step_end

CinnabarIsland_EventScript_BlackoutScene::
	lockall
	setvar VAR_TEMP_2, 2
	playse SE_M_EXPLOSION
	fadescreen FADE_TO_BLACK
	delay 40
	msgbox CinnabarIsland_Text_LightsOut
	fadescreen FADE_FROM_BLACK
	applymovement LOCALID_CHRONDROLIA_MAYOR, CinnabarIsland_Movement_MayorComes
	waitmovement 0
	applymovement LOCALID_CHRONDROLIA_MAYOR, Common_Movement_FaceRight
	waitmovement 0
	msgbox CinnabarIsland_Text_MayorReveal1
	msgbox CinnabarIsland_Text_MayorReveal2
	msgbox CinnabarIsland_Text_MayorReveal3
	closemessage
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_CHRONDROLIA_MAYOR
	delay 20
	fadescreen FADE_FROM_BLACK
	setflag FLAG_CHRONDROLIA_RAID_STARTED
	releaseall
	end

CinnabarIsland_EventScript_PlantWorker::
	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, CinnabarIsland_EventScript_PlantWorkerDone''')
sub(sp,'CinnabarIsland_EventScript_Scientist::\n','CinnabarIsland_EventScript_Scientist::\n	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, CinnabarIsland_EventScript_ScientistDone\n')
sub(sp,'CinnabarIsland_EventScript_LittleGirl::\n','CinnabarIsland_EventScript_LittleGirl::\n	goto_if_set FLAG_CHRONDROLIA_RAID_DONE, CinnabarIsland_EventScript_LittleGirlDone\n')
wr(sp,rd(sp).rstrip('\n')+'''

CinnabarIsland_EventScript_PlantWorkerDone::
	msgbox CinnabarIsland_Text_PlantWorkerDone, MSGBOX_NPC
	end

CinnabarIsland_EventScript_ScientistDone::
	msgbox CinnabarIsland_Text_ScientistDone, MSGBOX_NPC
	end

CinnabarIsland_EventScript_LittleGirlDone::
	msgbox CinnabarIsland_Text_LittleGirlDone, MSGBOX_NPC
	end
''')
addtext('data/maps/CinnabarIsland/text.inc',
 mktext('CinnabarIsland_Text_LightsOut',[["Every light in CHRONDROLIA just","died at once."]])+'\n'+
 mktext('CinnabarIsland_Text_MayorReveal1',[
 ["MAYOR: A fine badge, trainer. And","the SECRET KEY. Well done."],
 ["ONYBRIS needed one honest hand to","open the old vault under the PLANT."]])+'\n'+
 mktext('CinnabarIsland_Text_MayorReveal2',[
 ["The TOPAZ sleeps in the transformer","park. Its heat feeds the volcano."],
 ["SELENE is already there. And the","PLANT is ours. All of it."]])+'\n'+
 mktext('CinnabarIsland_Text_MayorReveal3',[
 ["Do not take it personally. The","MASTER pays far better than the"],
 ["council. Now, excuse me. I have a","lot of lights to switch on… later."]])+'\n'+
 mktext('CinnabarIsland_Text_PlantWorkerDone',[
 ["WORKER: Those 'workers' were","ONYBRIS for weeks!"],
 ["The grid is ours again. And the","lights are back on. Thanks, kid!"]])+'\n'+
 mktext('CinnabarIsland_Text_ScientistDone',[
 ["SCIENTIST: The cadre said the","eruption was their doing."],
 ["The coast guard lifted the sea","road ban. Be careful out there."]])+'\n'+
 mktext('CinnabarIsland_Text_LittleGirlDone',[["The pylon hums happy again!","Thank you!"]]))

# ---- Route 20 / Fuchsia reopen ----
sub('data/maps/Route20/scripts.inc','Route20_OnTransition::\n','Route20_OnTransition::\n	call_if_set FLAG_CHRONDROLIA_RAID_DONE, Route20_EventScript_SeaOpen\n')
wr('data/maps/Route20/scripts.inc',rd('data/maps/Route20/scripts.inc').rstrip('\n')+'''

Route20_EventScript_SeaOpen::
	setvar VAR_TEMP_1, 1
	return
''')
sub('data/maps/FuchsiaCity/scripts.inc','	call_if_set FLAG_BADGE05_GET, FuchsiaCity_EventScript_HidePolice\n','	call_if_set FLAG_BADGE05_GET, FuchsiaCity_EventScript_HidePolice\n	call_if_set FLAG_CHRONDROLIA_RAID_DONE, FuchsiaCity_EventScript_HideSouthPolice\n')
sub('data/maps/FuchsiaCity/scripts.inc','FuchsiaCity_EventScript_HidePolice::','FuchsiaCity_EventScript_HideSouthPolice::\n	setflag FLAG_TEMP_9\n	return\n\nFuchsiaCity_EventScript_HidePolice::')
print('applied')
