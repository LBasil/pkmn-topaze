#!/usr/bin/env python3
"""SEAFOAM volcano = QG #4 of 5. Gold + Silver (allies) meet the player on 1F, grunts on B1F-B3F, beaten-grunt NPCs (their passage),
KRONOS fought on B4F, Gold + Silver found beaten, boss gone (clue toward the last QG), Moltres replaces Articuno, fire/rock wild fauna.
Run once from repo root (marker: FLAG_SEAFOAM_ALLIES_MET)."""
import json,re,sys
if 'FLAG_SEAFOAM_ALLIES_MET' in open('include/constants/flags.h').read():
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
import os
def addtext(p,s):
    if not os.path.exists(p):
        wr(p,''); mp=p.split('/')[2]
        ev='data/event_scripts.s'; e=rd(ev); anchor='\t.include "data/maps/SeafoamIslands_B4F/text.inc"\n'
        inc='\t.include "%s"\n'%p
        if inc not in e: wr(ev,e.replace(anchor,anchor+inc,1))
    wr(p,(rd(p).rstrip('\n')+'\n\n' if rd(p) else '')+s)
def mj(n):
    p=f'data/maps/{n}/map.json'; return p,json.load(open(p))
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
def npc(local,gfx,x,y,script,flag,face='DOWN'):
    o={"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":script,"flag":flag}
    return {"local_id":local,**o} if local else o
def trainer(gfx,x,y,face,sight,script,flag):
    return {"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":str(sight),"script":script,"flag":flag}

# ---- flags ----
f='include/constants/flags.h'
sub(f,'#define FLAG_0x0B4               0x0B4','#define FLAG_SEAFOAM_ALLIES_MET  0x0B4')
sub(f,'#define FLAG_0x0B5               0x0B5','#define FLAG_SEAFOAM_BOSS_DONE   0x0B5')

# ---- trainers ----
GR=[('TRAINER_RS_TUBER_M','ROCKET_GRUNT_M',[('GOLBAT',42),('MUK',43),('MAGMAR',43)]),
    ('TRAINER_RS_TUBER_F','ROCKET_GRUNT_F',[('ARBOK',43),('VENOMOTH',42),('MAGCARGO',43)]),
    ('TRAINER_RS_GENTLEMAN','ROCKET_GRUNT_M',[('RAPIDASH',43),('WEEZING',44),('GOLBAT',42)]),
    ('TRAINER_RS_BEAUTY','ROCKET_GRUNT_F',[('HYPNO',43),('ARCANINE',44),('TENTACRUEL',43)]),
    ('TRAINER_RS_YOUNGSTER','ROCKET_GRUNT_M',[('MAGMAR',44),('ALAKAZAM',43),('MUK',44)]),
    ('TRAINER_RS_LADY','ROCKET_GRUNT_F',[('NIDOQUEEN',44),('NINETALES',44),('GENGAR',43)]),
    ('TRAINER_AQUA_ADMIN_MATT','MAGMA_ADMIN_M',[('ARBOK',47),('WEEZING',47),('NIDOKING',48),('CROBAT',48),('ALAKAZAM',50)])]
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
for tid,pic,team in GR:
    name='KRONOS' if 'MATT' in tid else 'GRUNT'
    b=re.search(r'\[%s\] = \{.*?\n    \},'%tid,tr,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_TEAM_ROCKET',b)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%pic,nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    if name=='KRONOS': nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT',nb)
    sym=re.search(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'NO_ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    tr=tr.replace(b,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    iv=60 if name=='KRONOS' else 30
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(iv,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)

M,F_='OBJ_EVENT_GFX_ROCKET_M','OBJ_EVENT_GFX_ROCKET_F'
GOLD,SILVER='OBJ_EVENT_GFX_RS_BRENDAN','OBJ_EVENT_GFX_BLUE'
def ensure_transition(mp,call):
    sp=f'data/maps/{mp}/scripts.inc'; s=rd(sp)
    if f'{mp}_OnTransition::' in s:
        s=s.replace(f'{mp}_OnTransition::\n',f'{mp}_OnTransition::\n\tcall {call}\n',1)
    else:
        s=s.replace('\t.byte 0\n',f'\tmap_script MAP_SCRIPT_ON_TRANSITION, {mp}_OnTransition\n\t.byte 0\n\n{mp}_OnTransition::\n\tcall {call}\n\tend\n',1)
    wr(sp,s)

# ================= 1F : Gold + Silver meet the player =================
p,m=mj('SeafoamIslands_1F')
W=[('LOCALID_SEAFOAM_GOLD_W',GOLD,5,16,'FLAG_TEMP_1'),('LOCALID_SEAFOAM_SILVER_W',SILVER,7,16,'FLAG_TEMP_2'),
   ('LOCALID_SEAFOAM_GOLD_E',GOLD,31,16,'FLAG_TEMP_3'),('LOCALID_SEAFOAM_SILVER_E',SILVER,33,16,'FLAG_TEMP_4')]
for loc,g,x,y,fl in W: m['object_events'].append(npc(loc,g,x,y,'SeafoamIslands_1F_EventScript_AllyStub',fl))
for x in (5,6,7): m['coord_events'].append({"type":"trigger","x":x,"y":19,"elevation":3,"var":"VAR_TEMP_1","var_value":"0","script":"SeafoamIslands_1F_EventScript_AlliesWest"})
for x in (31,32,33): m['coord_events'].append({"type":"trigger","x":x,"y":19,"elevation":3,"var":"VAR_TEMP_1","var_value":"0","script":"SeafoamIslands_1F_EventScript_AlliesEast"})
save(p,m)
sp='data/maps/SeafoamIslands_1F/scripts.inc'
sub(sp,'\tsetworldmapflag FLAG_WORLD_MAP_SEAFOAM_ISLANDS_1F\n\tend\n','''	setworldmapflag FLAG_WORLD_MAP_SEAFOAM_ISLANDS_1F
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_4
	goto_if_set FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_1F_EventScript_AlliesDone
	end

SeafoamIslands_1F_EventScript_AlliesDone::
	setvar VAR_TEMP_1, 1
	end

SeafoamIslands_1F_EventScript_AllyStub::
	end
''')
def meet(side,gl,sl,fg,fs):
    return f'''
SeafoamIslands_1F_EventScript_Allies{side}::
	lockall
	clearflag {fg}
	clearflag {fs}
	addobject {gl}
	addobject {sl}
	playse SE_PIN
	delay 20
	applymovement {gl}, SeafoamIslands_1F_Movement_AllyDown
	applymovement {sl}, SeafoamIslands_1F_Movement_AllyDown
	waitmovement 0
	msgbox SeafoamIslands_1F_Text_GoldMeet
	msgbox SeafoamIslands_1F_Text_SilverMeet
	msgbox SeafoamIslands_1F_Text_GoldPlan
	msgbox SeafoamIslands_1F_Text_SilverPlan
	closemessage
	applymovement {gl}, SeafoamIslands_1F_Movement_AllyUp
	applymovement {sl}, SeafoamIslands_1F_Movement_AllyUp
	waitmovement 0
	removeobject {gl}
	removeobject {sl}
	setflag FLAG_SEAFOAM_ALLIES_MET
	setvar VAR_TEMP_1, 1
	releaseall
	end
'''
s=rd(sp)
s+=meet('West','LOCALID_SEAFOAM_GOLD_W','LOCALID_SEAFOAM_SILVER_W','FLAG_TEMP_1','FLAG_TEMP_2')
s+=meet('East','LOCALID_SEAFOAM_GOLD_E','LOCALID_SEAFOAM_SILVER_E','FLAG_TEMP_3','FLAG_TEMP_4')
s+='''
SeafoamIslands_1F_Movement_AllyDown::
	walk_down
	walk_down
	step_end

SeafoamIslands_1F_Movement_AllyUp::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end
'''
wr(sp,s)
addtext('data/maps/SeafoamIslands_1F/text.inc',
 mktext('SeafoamIslands_1F_Text_GoldMeet',[["GOLD: Hey! You are the kid from","HEMATOWN, right? I am GOLD."],["That grumpy one is SILVER."]])+'\n'+
 mktext('SeafoamIslands_1F_Text_SilverMeet',[["SILVER: …Tch. I can introduce","myself, you know."],["I heard what you did to KRONOS.","Not bad. For a beginner."]])+'\n'+
 mktext('SeafoamIslands_1F_Text_GoldPlan',[["GOLD: This volcano is ONYBRIS base","number four. The boss went down"],["with the stone. We follow him","all the way to the bottom."],["BRICE and FLORA fell to him.","We will not."]])+'\n'+
 mktext('SeafoamIslands_1F_Text_SilverPlan',[["SILVER: Stay behind us, {PLAYER}.","We take the lower floors first."],["Mop up the grunts we leave.","And do not die on me."]]))

# ================= B1F / B2F / B3F : grunts + beaten NPCs =================
FL=['FLAG_TEMP_4','FLAG_TEMP_5','FLAG_TEMP_6']
LAYS=[('SeafoamIslands_B1F',[('TRAINER_RS_TUBER_M',M,15,13,'DOWN',4,'1',["Nobody enters our volcano!"],["Burned out…"],["BASE NUMBER FOUR is ours. Deeper","down, the big shots are waiting."]),
                             ('TRAINER_RS_TUBER_F',F_,30,6,'LEFT',4,'2',["This is a restricted lava field!"],["That was hot…"],["Two kids in caps went by earlier.","Be glad you are not them."])],None),
      ('SeafoamIslands_B2F',[('TRAINER_RS_GENTLEMAN',M,14,10,'DOWN',4,'3',["The volcano is a fine hideout.","Warm and no neighbors."],["I lost my composure…"],["Take a gentleman's advice:","do not go any deeper."]),
                             ('TRAINER_RS_BEAUTY',F_,31,10,'LEFT',4,'4',["You smell like a lawman's kid!"],["Hmph. Ugly loss."],["The boss walked right past us.","We were told not to look."])],
       ('LOCALID_SEAFOAM_B2F_BEATEN',M,21,10,'SeafoamIslands_B2F_EventScript_BeatenGrunt','SeafoamIslands_B2F_Text_BeatenGrunt',[["A kid in a cap went through here.","He wiped out my whole team…"],["Go on. The cap kid is ahead,","with a redhead."]])),
      ('SeafoamIslands_B3F',[('TRAINER_RS_YOUNGSTER',M,15,12,'DOWN',4,'5',["No further! The lava is deep","and so is our loyalty!"],["Overcooked…"],["KRONOS is on the lowest floor.","He is in a bad mood."]),
                             ('TRAINER_RS_LADY',F_,21,5,'DOWN',4,'6',["You made it this far? Impressive!","But KRONOS awaits."],["Oh dear…"],["The two before you did not even","say hello. They just burned us."])],
       ('LOCALID_SEAFOAM_B3F_BEATEN',F_,17,7,'SeafoamIslands_B3F_EventScript_BeatenGrunt','SeafoamIslands_B3F_Text_BeatenGrunt',[["The redhead did not even speak.","He just took us apart."],["The boss is waiting at the","bottom. Brace yourself."]]))]
for mp,grunts,beaten in LAYS:
    p,m=mj(mp)
    for (tid,gfx,x,y,d,sight,lab,intro,defeat,post) in grunts:
        m['object_events'].append(trainer(gfx,x,y,d,sight,f'{mp}_EventScript_Onybris{lab}','FLAG_TEMP_5'))
    if beaten:
        loc,gfx,x,y,scr,txt,box=beaten
        m['object_events'].append(npc(loc,gfx,x,y,scr,'FLAG_TEMP_6'))
    save(p,m)
    sp=f'data/maps/{mp}/scripts.inc'
    ensure_transition(mp,f'{mp}_EventScript_HideOnybris')
    s=rd(sp)
    s+=f'''
{mp}_EventScript_HideOnybris::
	goto_if_unset FLAG_SEAFOAM_ALLIES_MET, {mp}_EventScript_HideBeaten
	goto_if_set FLAG_SEAFOAM_BOSS_DONE, {mp}_EventScript_HideBeaten
	return

{mp}_EventScript_HideBeaten::
	setflag FLAG_TEMP_6
	return
'''
    for (tid,gfx,x,y,d,sight,lab,intro,defeat,post) in grunts:
        s+=f'''
{mp}_EventScript_Onybris{lab}::
	trainerbattle_single {tid}, {mp}_Text_Onybris{lab}Intro, {mp}_Text_Onybris{lab}Defeat
	msgbox {mp}_Text_Onybris{lab}Post, MSGBOX_AUTOCLOSE
	end
'''
        addtext(f'data/maps/{mp}/text.inc',mktext(f'{mp}_Text_Onybris{lab}Intro',[intro])+'\n'+mktext(f'{mp}_Text_Onybris{lab}Defeat',[defeat])+'\n'+mktext(f'{mp}_Text_Onybris{lab}Post',[post]))
    if beaten:
        s+=f'\n{beaten[4]}::\n\tmsgbox {beaten[5]}, MSGBOX_NPC\n\tend\n'
        addtext(f'data/maps/{mp}/text.inc',mktext(beaten[5],beaten[6]))
    wr(sp,s)

# ================= B4F : Kronos, Gold + Silver beaten, Moltres =================
p,m=mj('SeafoamIslands_B4F')
for o in m['object_events']:
    if o['graphics_id']=='OBJ_EVENT_GFX_ARTICUNO': o['graphics_id']='OBJ_EVENT_GFX_MOLTRES'
m['object_events']+= [npc('LOCALID_SEAFOAM_KRONOS',F_.replace('F','M') if False else 'OBJ_EVENT_GFX_GIOVANNI',13,6,'SeafoamIslands_B4F_EventScript_AllyStub','FLAG_TEMP_1'),
    npc('LOCALID_SEAFOAM_GOLD_B4',GOLD,15,6,'SeafoamIslands_B4F_EventScript_GoldBeaten','FLAG_TEMP_2'),
    npc('LOCALID_SEAFOAM_SILVER_B4',SILVER,16,6,'SeafoamIslands_B4F_EventScript_SilverBeaten','FLAG_TEMP_3')]
save(p,m)
sp='data/maps/SeafoamIslands_B4F/scripts.inc'; s=rd(sp)
s=s.replace('SeafoamIslands_B4F_OnTransition::\n','SeafoamIslands_B4F_OnTransition::\n\tcall SeafoamIslands_B4F_EventScript_CheckOnybris\n',1)
s=s.replace('\tmap_script_2 VAR_TEMP_1, 1, SeafoamIslands_B4F_EventScript_EnterByFalling\n','\tmap_script_2 VAR_TEMP_1, 1, SeafoamIslands_B4F_EventScript_EnterByFalling\n\tmap_script_2 VAR_TEMP_3, 1, SeafoamIslands_B4F_EventScript_KronosScene\n',1)
# Moltres instead of Articuno
s=s.replace('SPECIES_ARTICUNO','SPECIES_MOLTRES').replace('setwildbattle SPECIES_MOLTRES, 50','setwildbattle SPECIES_MOLTRES, 55')
s+='''
SeafoamIslands_B4F_EventScript_AllyStub::
	end

SeafoamIslands_B4F_EventScript_CheckOnybris::
	goto_if_set FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B4F_EventScript_OnybrisDone
	goto_if_unset FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_B4F_EventScript_OnybrisDone
	setvar VAR_TEMP_3, 1
	return

SeafoamIslands_B4F_EventScript_OnybrisDone::
	setflag FLAG_TEMP_1
	goto_if_unset FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B4F_EventScript_OnybrisHideAll
	return

SeafoamIslands_B4F_EventScript_OnybrisHideAll::
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	return

SeafoamIslands_B4F_EventScript_KronosScene::
	lockall
	msgbox SeafoamIslands_B4F_Text_FloorScene
	msgbox SeafoamIslands_B4F_Text_KronosIntro
	closemessage
	setvar VAR_LAST_TALKED, LOCALID_SEAFOAM_KRONOS
	trainerbattle_no_intro TRAINER_AQUA_ADMIN_MATT, SeafoamIslands_B4F_Text_KronosDefeat
	msgbox SeafoamIslands_B4F_Text_KronosPost
	closemessage
	playse SE_THUNDER
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	special ShakeScreen
	waitstate
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_SEAFOAM_KRONOS
	delay 20
	fadescreen FADE_FROM_BLACK
	msgbox SeafoamIslands_B4F_Text_GoldAfterScene
	msgbox SeafoamIslands_B4F_Text_SilverAfterScene
	closemessage
	setflag FLAG_SEAFOAM_BOSS_DONE
	setvar VAR_TEMP_3, 0
	releaseall
	end

SeafoamIslands_B4F_EventScript_GoldBeaten::
	msgbox SeafoamIslands_B4F_Text_GoldBeaten, MSGBOX_NPC
	end

SeafoamIslands_B4F_EventScript_SilverBeaten::
	msgbox SeafoamIslands_B4F_Text_SilverBeaten, MSGBOX_NPC
	end
'''
wr(sp,s)
addtext('data/maps/SeafoamIslands_B4F/text.inc',
 mktext('SeafoamIslands_B4F_Text_FloorScene',[["The air is scorching. Two figures","lie on the basalt, unmoving."],["GOLD and SILVER! Their POKéMON","are fainted. A shadow stands over","them… no, it has already left."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_KronosIntro',[["KRONOS: Late again, child.","The MASTER was here. Briefly."],["Those two charged him head on.","They lasted one move each."],["He took the stone and left. I","stayed to teach you manners."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_KronosDefeat',[["…Impossible.","The fire did not even slow you."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_KronosPost',[["KRONOS: Enough. The stone is on","its way to the LAST BASE."],["Where the road ends and the","LEAGUE begins. Come if you dare."],["The master waits for the one who","can burn brighter than lava."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_GoldAfterScene',[["GOLD: ugh… Is he gone? I could","not even see his hand move."],["One POKéMON, {PLAYER}. And it did","not even look at us."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_SilverAfterScene',[["SILVER: …Don't gloat. Your turn","is coming. Get stronger."],["The last base is near the LEAGUE.","We will get there. Before you."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_GoldBeaten',[["GOLD: Heal up and keep going.","I will catch up. Eventually."]])+'\n'+
 mktext('SeafoamIslands_B4F_Text_SilverBeaten',[["SILVER: Do not look at me like","that. Go and finish the job."]]))

# ================= wild fauna retheme (fire / rock) =================
wp='src/data/wild_encounters.json'; j=json.load(open(wp))
MAPL={'PSYDUCK':'SLUGMA','SLOWPOKE':'SLUGMA','GOLDUCK':'MAGCARGO','SLOWBRO':'MAGCARGO','SEEL':'GEODUDE','DEWGONG':'GRAVELER',
      'MAGIKARP':'SLUGMA','KRABBY':'SLUGMA','HORSEA':'TORKOAL','GYARADOS':'MAGCARGO'}
n=0
for g in j['wild_encounter_groups']:
    for e in g['encounters']:
        if e.get('map','').startswith('MAP_SEAFOAM_ISLANDS'):
            for k,v in e.items():
                if not isinstance(v,dict): continue
                for mon in v['mons']:
                    sp_=mon['species'][8:]
                    if sp_ in MAPL: mon['species']='SPECIES_'+MAPL[sp_]
                    if k in ('land_mons','water_mons'):
                        mon['min_level']+=6; mon['max_level']+=6
                    n+=1
json.dump(j,open(wp,'w'),indent=2); open(wp,'a').write('\n')
print('ok',n)
