#!/usr/bin/env python3
"""ROUTE VICTOIRE = dernier QG (n°5). Red (muet) entre dans la grotte devant le joueur ; sbires dans les 2 premiers etages, VESPER (3e duel) a la sortie est ;
Red retrouve a la sortie : l'ombre du patron s'enfuit vers le Plateau Indigo. Lancer une fois (marqueur FLAG_VR_RED_MET)."""
import json,re,sys
if 'FLAG_VR_RED_MET' in open('include/constants/flags.h').read(): print('already'); sys.exit(0)
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
def sub(p,old,new):
    s=rd(p); assert old in s,(p,old[:60]); wr(p,s.replace(old,new,1))
def mktext(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            assert len(re.sub(r'\{[^}]*\}','X',l))<=35,(len(l),l)
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
def mj(n):
    p=f'data/maps/{n}/map.json'; return p,json.load(open(p))
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
def addtext(p,s): wr(p,rd(p).rstrip('\n')+'\n\n'+s)
def replace_text(path,label,boxes):
    t=rd(path); a=t.index(label+'::'); b=t.find('\n\n',a); b=len(t) if b<0 else b
    wr(path,t[:a]+mktext(label,boxes).rstrip('\n')+t[b:])
f='include/constants/flags.h'
sub(f,'#define FLAG_0x0B6               0x0B6','#define FLAG_VR_RED_MET          0x0B6')
sub(f,'#define FLAG_0x0B7               0x0B7','#define FLAG_VR_BOSS_DONE        0x0B7')

# ---- trainers ----
G=[('COOLTRAINER_ROLANDO','ROCKET_GRUNT_M',[('MUK',50),('WEEZING',51),('ARBOK',51)]),
   ('COOLTRAINER_NAOMI','ROCKET_GRUNT_F',[('GENGAR',50),('TENTACRUEL',51),('VENOMOTH',51)]),
   ('POKEMANIAC_DAWSON','ROCKET_GRUNT_M',[('CROBAT',51),('ALAKAZAM',52),('HYPNO',51)]),
   ('BLACK_BELT_DAISUKE','ROCKET_GRUNT_M',[('MACHAMP',52),('MAGMAR',52),('NIDOKING',52)]),
   ('JUGGLER_NELSON','ROCKET_GRUNT_F',[('ELECTABUZZ',52),('WEEZING',52),('MUK',52)]),
   ('TAMER_VINCENT','ROCKET_GRUNT_M',[('HYPNO',52),('ARCANINE',52),('GENGAR',52)]),
   ('JUGGLER_GREGORY','ROCKET_GRUNT_M',[('CROBAT',52),('TENTACRUEL',52),('RAPIDASH',53)]),
   ('MAGMA_ADMIN_TABITHA','MAGMA_ADMIN_F',[('ARBOK',54),('GENGAR',54),('CROBAT',55),('MUK',55),('HYPNO',56)])]
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
for t,pic,team in G:
    b=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%t,tr,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_TEAM_ROCKET',b)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%pic,nb)
    vesper='TABITHA' in t
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%('VESPER' if vesper else 'GRUNT'),nb)
    if vesper: nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT',nb)
    sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'(?:NO_)?ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    tr=tr.replace(b,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    iv=60 if vesper else 30
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(iv,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)

# ---- grunts in VR 1F/2F : sprites + texts ----
GFX={'ROLANDO':'M','NAOMI':'F','DAWSON':'M','DAISUKE':'M','NELSON':'F','VINCENT':'M','GREGORY':'M'}
TX={('1F','Rolando'):(["The League road belongs to us!"],["Burned out."],["The MASTER is ahead. RED went","in before you. Alone."]),
    ('1F','Naomi'):(["No challengers today, kid."],["You are a pest…"],["That silent kid in red walked","right past us. Scary."]),
    ('2F','Dawson'):(["We took the whole cave. Even the","trainers ran away."],["Lights out…"],["Strongest in KANTO, they say.","He did not even draw a weapon."]),
    ('2F','Daisuke'):(["Fists or POKéMON, I do not mind!"],["Knocked flat!"],["The last base is ours. Not for","long, it seems."]),
    ('2F','Nelson'):(["Hehe! Watch my POKéMON dance!"],["Show is over…"],["Everyone on the exit side fears","VESPER. Be careful."]),
    ('2F','Vincent'):(["Lost? Then follow my POKéMON!"],["I lost my way…"],["The way out is east. VESPER","waits there."]),
    ('2F','Gregory'):(["Welcome to the back door!"],["Doors slam…"],["The MASTER used this cave as his","stage. We only guard it."])}
for fl,po in (('1F','VictoryRoad_1F'),('2F','VictoryRoad_2F')):
    p,m=mj(po)
    for o in m['object_events']:
        for k,g in GFX.items():
            if o['script'].endswith('_'+k.title()):
                o['graphics_id']='OBJ_EVENT_GFX_ROCKET_'+g
    save(p,m)
    for (flr,nm),(a,b,c) in TX.items():
        if flr!=fl: continue
        tp=f'data/maps/{po}/text.inc'
        replace_text(tp,f'{po}_Text_{nm}Intro',[a]); replace_text(tp,f'{po}_Text_{nm}Defeat',[b]); replace_text(tp,f'{po}_Text_{nm}PostBattle',[c])

# ---- VESPER at 2F exit ----
p,m=mj('VictoryRoad_2F')
m['object_events'].append({"type":"object","graphics_id":"OBJ_EVENT_GFX_ROCKET_F","x":46,"y":14,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_LEFT","movement_range_x":0,"movement_range_y":0,
 "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"5","script":"VictoryRoad_2F_EventScript_Vesper","flag":"0"})
save(p,m)
sp='data/maps/VictoryRoad_2F/scripts.inc'; wr(sp,rd(sp)+'''
VictoryRoad_2F_EventScript_Vesper::
	trainerbattle_single TRAINER_MAGMA_ADMIN_TABITHA, VictoryRoad_2F_Text_VesperIntro, VictoryRoad_2F_Text_VesperDefeat
	msgbox VictoryRoad_2F_Text_VesperPost, MSGBOX_AUTOCLOSE
	end
''')
addtext('data/maps/VictoryRoad_2F/text.inc',
 mktext('VictoryRoad_2F_Text_VesperIntro',[["VESPER: Third time, child.","I almost admire your stubbornness."],["The MASTER left through this very","door, and the red-capped one is"],["already outside, licking his","wounds. You will not follow!"]])+'\n'+
 mktext('VictoryRoad_2F_Text_VesperDefeat',[["…Again. Again you break the","pattern."]])+'\n'+
 mktext('VictoryRoad_2F_Text_VesperPost',[["VESPER: Go, then. The LEAGUE needs","a witness. Not a hero."],["The stones are almost all gathered.","What comes next is not for us."]]))

# ---- Route 23 : Red enters / Red waits at the end ----
p,m=mj('Route23')
def npc(loc,gfx,x,y,flag,face):
    return {"local_id":loc,"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
            "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":"Route23_EventScript_RedStub","flag":flag}
m['object_events'].append(npc('LOCALID_VR_RED_CAVE','OBJ_EVENT_GFX_RED_NORMAL',5,29,'FLAG_TEMP_1','UP'))
m['object_events'].append(npc('LOCALID_VR_RED_END','OBJ_EVENT_GFX_RED_NORMAL',20,19,'FLAG_TEMP_2','DOWN'))
for x in range(2,9): m['coord_events'].append({"type":"trigger","x":x,"y":32,"elevation":3,"var":"VAR_TEMP_4","var_value":"0","script":"Route23_EventScript_RedAtCave"})
for x in (19,20,21): m['coord_events'].append({"type":"trigger","x":x,"y":22,"elevation":3,"var":"VAR_TEMP_5","var_value":"0","script":"Route23_EventScript_RedAtEnd"})
save(p,m)
sp='data/maps/Route23/scripts.inc'
sub(sp,'\tsetvar VAR_MAP_SCENE_VICTORY_ROAD_3F, 0\n\tend\n','''	setvar VAR_MAP_SCENE_VICTORY_ROAD_3F, 0
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	goto_if_set FLAG_VR_RED_MET, Route23_EventScript_RedCaveDone
	goto Route23_EventScript_RedEndNotYet
	end

Route23_EventScript_RedCaveDone::
	setvar VAR_TEMP_4, 1
	goto_if_set FLAG_VR_BOSS_DONE, Route23_EventScript_RedEndDone
	goto Route23_EventScript_RedEndNotYet
	end

Route23_EventScript_RedEndDone::
	setvar VAR_TEMP_5, 1
	end

Route23_EventScript_RedEndNotYet::
	end

Route23_EventScript_RedStub::
	end

Route23_EventScript_RedAtCave::
	lockall
	clearflag FLAG_TEMP_1
	addobject LOCALID_VR_RED_CAVE
	playse SE_PIN
	delay 20
	applymovement LOCALID_VR_RED_CAVE, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox Route23_Text_RedStares
	msgbox Route23_Text_RedSilent
	msgbox Route23_Text_RedEnters
	closemessage
	applymovement LOCALID_VR_RED_CAVE, Route23_Movement_RedIn
	waitmovement 0
	removeobject LOCALID_VR_RED_CAVE
	setflag FLAG_VR_RED_MET
	setvar VAR_TEMP_4, 1
	releaseall
	end

Route23_Movement_RedIn::
	walk_up
	step_end

Route23_EventScript_RedAtEnd::
	lockall
	goto_if_unset FLAG_VR_RED_MET, Route23_EventScript_RedAtEndSkip
	clearflag FLAG_TEMP_2
	addobject LOCALID_VR_RED_END
	delay 20
	msgbox Route23_Text_RedEndA
	msgbox Route23_Text_RedEndB
	msgbox Route23_Text_RedSilent
	msgbox Route23_Text_RedEndC
	closemessage
	applymovement LOCALID_VR_RED_END, Route23_Movement_RedWalkNorth
	waitmovement 0
	removeobject LOCALID_VR_RED_END
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_5, 1
	releaseall
	end

Route23_EventScript_RedAtEndSkip::
	setvar VAR_TEMP_5, 1
	releaseall
	end

Route23_Movement_RedWalkNorth::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end
''')
addtext('data/maps/Route23/text.inc',
 mktext('Route23_Text_RedStares',[["A trainer in a red cap stands at","the cave mouth, staring into the","dark."]])+'\n'+
 mktext('Route23_Text_RedSilent',[["RED: ……"]])+'\n'+
 mktext('Route23_Text_RedEnters',[["He looks at you for a long moment,","tips his cap, and walks into the","VICTORY ROAD alone."]])+'\n'+
 mktext('Route23_Text_RedEndA',[["RED waits at the end of the road.","His cap is torn. His hands shake."]])+'\n'+
 mktext('Route23_Text_RedEndB',[["High above the PLATEAU a black","shape rises and fades into the","clouds. The MASTER is gone."]])+'\n'+
 mktext('Route23_Text_RedEndC',[["He did not win. Nobody could.","But he nods to you, once."],["Then he picks up his cap and walks","on toward the POKéMON LEAGUE."]]))
print('ok')
