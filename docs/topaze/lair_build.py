#!/usr/bin/env python3
"""LE REPAIRE d'ONYBRIS sous la ROUTE VICTOIRE (QG n°5) : 3 salles (Salle des gardes / Salle des Pierres / Salle du trone), echelle d'acces au 2F,
sorties de la grotte verrouillees tant que le patron n'est pas passe. Remplace le finale provisoire du 2F. Lancer apres lair_tileset.py et lair_layouts.py. Idempotent (marqueur)."""
import json,re,sys,struct
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
if 'FLAG_LAIR_ITEM_1' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
def sub(p,old,new):
    s=rd(p); assert old in s,(p,old[:60]); wr(p,s.replace(old,new,1))
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(re.sub(r'\{[^}]*\}','X',l))<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
# ---- flags ----
f='include/constants/flags.h'
sub(f,'#define FLAG_0x0B8               0x0B8','#define FLAG_LAIR_ITEM_1         0x0B8')
sub(f,'#define FLAG_0x0B9               0x0B9','#define FLAG_LAIR_ITEM_2         0x0B9')
# ---- trainers ----
G=[('RS_COOLTRAINER_M','ROCKET_GRUNT_M',[('WEEZING',53),('CROBAT',54),('ALAKAZAM',54)],0),
   ('RS_COOLTRAINER_F','ROCKET_GRUNT_F',[('GENGAR',53),('TENTACRUEL',54),('ARBOK',54)],0),
   ('RS_BLACK_BELT','ROCKET_GRUNT_M',[('MACHAMP',54),('MUK',54),('MAGMAR',54)],0),
   ('RS_RUIN_MANIAC','ROCKET_GRUNT_M',[('HYPNO',54),('RAPIDASH',54),('NIDOKING',54)],0),
   ('RS_POKEMANIAC','ROCKET_GRUNT_F',[('VENOMOTH',54),('ARCANINE',54),('ELECTABUZZ',54)],0),
   ('RS_AROMA_LADY','MAGMA_ADMIN_F',[('HYPNO',56),('MUK',56),('VENOMOTH',56),('TENTACRUEL',57),('GENGAR',58),('ALAKAZAM',58)],1)]
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
for t,pic,team,boss in G:
    b=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%t,tr,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_TEAM_ROCKET',b)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_AQUA',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%pic,nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%('SELENE' if boss else 'GRUNT'),nb)
    if boss: nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT',nb)
    sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'(?:NO_)?ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    tr=tr.replace(b,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    iv=60 if boss else 30
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(iv,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)

# ---- map builder ----
def mapjson(name,layout,warps,objs,coords=(),bgs=()):
    return {"id":"MAP_"+re.sub(r'(?<!^)(?=[A-Z0-9])','_',name).upper().replace('__','_'),"name":name,"layout":layout,"music":"MUS_ROCKET_HIDEOUT",
      "region_map_section":"MAPSEC_VICTORY_ROAD","requires_flash":False,"weather":"WEATHER_NONE","map_type":"MAP_TYPE_INDOOR","allow_cycling":False,"allow_escaping":False,
      "allow_running":True,"show_map_name":True,"floor_number":0,"battle_scene":"MAP_BATTLE_SCENE_NORMAL","connections":None,
      "object_events":list(objs),"warp_events":[dict(x=x,y=y,elevation=0,dest_map=dm,dest_warp_id=str(di)) for (x,y,dm,di) in warps],
      "coord_events":list(coords),"bg_events":list(bgs)}
def npc(gfx,x,y,script,flag='0',face='DOWN',local=None):
    o={"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":script,"flag":flag}
    return {"local_id":local,**o} if local else o
def trainer(gfx,x,y,face,sight,script):
    return {"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face,"movement_range_x":0,"movement_range_y":0,
       "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":str(sight),"script":script,"flag":"0"}
def sign(x,y,script): return {"type":"sign","x":x,"y":y,"elevation":0,"player_facing_dir":"BG_EVENT_PLAYER_FACING_ANY","script":script}
M1,M2,M3='VictoryRoadLair_1F','VictoryRoadLair_2F','VictoryRoadLair_3F'
GM,GF='OBJ_EVENT_GFX_ROCKET_M','OBJ_EVENT_GFX_ROCKET_F'
# ---------- 1F : Salle des gardes ----------
P='VictoryRoadLair_1F'
objs1=[trainer(GM,4,19,'RIGHT',4,P+'_EventScript_Grunt1'),trainer(GF,9,20,'UP',4,P+'_EventScript_Grunt2'),trainer(GM,13,18,'LEFT',4,P+'_EventScript_Grunt3'),
       trainer(GM,18,17,'DOWN',3,P+'_EventScript_Grunt4'),trainer(GF,22,11,'LEFT',4,P+'_EventScript_Grunt5'),
       trainer(GF,6,7,'DOWN',4,P+'_EventScript_Vesper'),
       npc('OBJ_EVENT_GFX_ITEM_BALL',25,10,P+'_EventScript_ItemMaxRevive','FLAG_LAIR_ITEM_1'),
       npc('OBJ_EVENT_GFX_ITEM_BALL',2,7,P+'_EventScript_ItemRareCandy','FLAG_LAIR_ITEM_2')]
w1=[(14,21,'MAP_VICTORY_ROAD_2F',9),(15,21,'MAP_VICTORY_ROAD_2F',9),(6,5,M2.join(['MAP_','']).replace('MAP_VictoryRoadLair_2F','MAP_VICTORY_ROAD_LAIR_2F'),0)]
# ---------- 2F : Salle des Pierres ----------
STONES=[('GRENAT',4,5,True),('PYROPE',6,5,True),('TOURMALINE',8,5,True),('APATITE',3,7,False),('SPINELLE',9,7,True),('TOPAZ',3,9,False),
        ('QUARTZ',9,9,True),('AMETHIOLITE',4,11,True),('HEMATITE',6,11,True),('OPAL',8,11,False)]
P2='VictoryRoadLair_2F'
objs2=[trainer(GF,7,3,'LEFT',1,P2+'_EventScript_Selene')]; bgs2=[]
for nm,x,y,here in STONES:
    if here: objs2.append(npc('OBJ_EVENT_GFX_METEORITE',x,y,f'{P2}_EventScript_Stone{nm.title()}'))
    else: bgs2.append(sign(x,y,f'{P2}_EventScript_Pedestal{nm.title()}'))
w2=[(6,19,'MAP_VICTORY_ROAD_LAIR_1F',2),(6,2,'MAP_VICTORY_ROAD_LAIR_3F',0)]
# ---------- 3F : Salle du trone ----------
P3='VictoryRoadLair_3F'
objs3=[npc('OBJ_EVENT_GFX_RED_NORMAL',6,6,P3+'_EventScript_Red','0','UP','LOCALID_LAIR_RED')]
coords3=[{"type":"trigger","x":x,"y":10,"elevation":3,"var":"VAR_TEMP_1","var_value":"0","script":P3+"_EventScript_FinalScene"} for x in range(1,12)]
w3=[(6,12,'MAP_VICTORY_ROAD_LAIR_2F',1)]
for nm,lay,warps,objs,coords,bgs in ((M1,'LAYOUT_VICTORY_ROAD_LAIR_1F',w1,objs1,[],[]),(M2,'LAYOUT_VICTORY_ROAD_LAIR_2F',w2,objs2,[],bgs2),(M3,'LAYOUT_VICTORY_ROAD_LAIR_3F',w3,objs3,coords3,[])):
    import os; os.makedirs('data/maps/'+nm,exist_ok=True)
    mp=mapjson(nm,lay,warps,objs,coords,bgs)
    mp['id']={'VictoryRoadLair_1F':'MAP_VICTORY_ROAD_LAIR_1F','VictoryRoadLair_2F':'MAP_VICTORY_ROAD_LAIR_2F','VictoryRoadLair_3F':'MAP_VICTORY_ROAD_LAIR_3F'}[nm]
    save(f'data/maps/{nm}/map.json',mp)
# registration
f='data/maps/map_groups.json'; s=rd(f)
j=json.loads(s); lst=j['gMapGroup_Dungeons']
for nm in (M1,M2,M3):
    if nm not in lst: lst.append(nm)
j['gMapGroup_Dungeons']=lst; wr(f,json.dumps(j,indent=2)+'\n')
f='data/event_scripts.s'; s=rd(f)
for kind,anchor in (('scripts','\t.include "data/maps/VictoryRoad_3F/scripts.inc"\n'),('text','\t.include "data/maps/VictoryRoad_3F/text.inc"\n')):
    add=''.join('\t.include "data/maps/%s/%s.inc"\n'%(nm,kind) for nm in (M1,M2,M3)); assert anchor in s; s=s.replace(anchor,anchor+add,1)
wr(f,s)
# step warps
sub('src/field_control_avatar.c','|| gMapHeader.mapLayoutId == LAYOUT_POKEMON_MANSION_1F','|| gMapHeader.mapLayoutId == LAYOUT_VICTORY_ROAD_LAIR_1F || gMapHeader.mapLayoutId == LAYOUT_VICTORY_ROAD_LAIR_2F || gMapHeader.mapLayoutId == LAYOUT_VICTORY_ROAD_LAIR_3F\n        || gMapHeader.mapLayoutId == LAYOUT_POKEMON_MANSION_1F')

# ---------- scripts + texts ----------
GR={'Grunt1':('RS_COOLTRAINER_M',["This hall is the MASTER's. Turn","back while you still can!"],["Burnt out."],["The lair is a maze of statues.","The Hall of Stones is north."]),
    'Grunt2':('RS_COOLTRAINER_F',["You came through the CAVE? Then","you are the one the boss expects."],["He was right about you…"],["Do not touch the stones. They","bite."]),
    'Grunt3':('RS_BLACK_BELT',["Fists first, questions later!"],["Beaten by a kid!"],["The red-capped boy went up the","stairs on his own. We let him."]),
    'Grunt4':('RS_RUIN_MANIAC',["Ruins, relics, ritual! You do not","belong in this one!"],["The ritual is broken…"],["Ten stones, ten seats. The boss","only needs two more."]),
    'Grunt5':('RS_POKEMANIAC',["The treasure room is mine!"],["My treasure!"],["Take it. It is only a medicine","chest. The real prize is upstairs."])}
scr=f'{P}_MapScripts::\n\t.byte 0\n'
txt=''
for k,(tid,a,b,c) in GR.items():
    scr+=f'\n{P}_EventScript_{k}::\n\ttrainerbattle_single TRAINER_{tid}, {P}_Text_{k}Intro, {P}_Text_{k}Defeat\n\tmsgbox {P}_Text_{k}Post, MSGBOX_AUTOCLOSE\n\tend\n'
    txt+=box(f'{P}_Text_{k}Intro',[a])+'\n'+box(f'{P}_Text_{k}Defeat',[b])+'\n'+box(f'{P}_Text_{k}Post',[c])+'\n'
scr+=f'''
{P}_EventScript_Vesper::
	trainerbattle_single TRAINER_MAGMA_ADMIN_TABITHA, {P}_Text_VesperIntro, {P}_Text_VesperDefeat
	msgbox {P}_Text_VesperPost, MSGBOX_AUTOCLOSE
	end

{P}_EventScript_ItemMaxRevive::
	finditem ITEM_MAX_REVIVE
	end

{P}_EventScript_ItemRareCandy::
	finditem ITEM_RARE_CANDY
	end
'''
txt+=box(P+'_Text_VesperIntro',[["VESPER: Third time, child. Do you","know where you are standing?"],["The MASTER's HALL. The old","heroes died on that threshold."],["I will not let you pass it."]])+'\n'
txt+=box(P+'_Text_VesperDefeat',[["…Again. Again you break the","pattern."]])+'\n'
txt+=box(P+'_Text_VesperPost',[["VESPER: The red-capped one is in","the HALL of STONES, then beyond."],["Go. SELENE keeps the door."]])
wr(f'data/maps/{M1}/scripts.inc',scr); wr(f'data/maps/{M1}/text.inc',txt.rstrip('\n')+'\n')
# 2F
scr=f'{P2}_MapScripts::\n\t.byte 0\n'; txt=''
scr+=f'''
{P2}_EventScript_Selene::
	trainerbattle_single TRAINER_RS_AROMA_LADY, {P2}_Text_SeleneIntro, {P2}_Text_SeleneDefeat
	msgbox {P2}_Text_SelenePost, MSGBOX_AUTOCLOSE
	end
'''
txt+=box(P2+'_Text_SeleneIntro',[["SELENE: The HALL of STONES. Seven","gather here, three are missing."],["APATITE, TOPAZ, OPAL. You hold","one. The boy in red carried the"],["other. The MASTER will have","them all. Over my dead body? No."],["Over yours."]])+'\n'
txt+=box(P2+'_Text_SeleneDefeat',[["…Fine. Go and see for yourself."]])+'\n'
txt+=box(P2+'_Text_SelenePost',[["SELENE: Go up. The THRONE ROOM","is beyond that door."],["Whatever you find, remember: we","only wanted the POKéMON free."]])+'\n'
for nm,x,y,here in STONES:
    N=nm.title()
    if here:
        scr+=f'\n{P2}_EventScript_Stone{N}::\n\tmsgbox {P2}_Text_Stone{N}, MSGBOX_SIGN\n\tend\n'
    else:
        scr+=f'\n{P2}_EventScript_Pedestal{N}::\n\tmsgbox {P2}_Text_Pedestal{N}, MSGBOX_SIGN\n\tend\n'
    if here: txt+=box(f'{P2}_Text_Stone{N}',[[f"The {nm} STONE rests","on a black pedestal."],["It was taken from its town.","It pulses, as if it wanted home."]])+'\n'
    else: txt+=box(f'{P2}_Text_Pedestal{N}',[[f"An empty pedestal. Carved on it:",f"{nm}."],["Something is meant to rest here."]])+'\n'
wr(f'data/maps/{M2}/scripts.inc',scr); wr(f'data/maps/{M2}/text.inc',txt.rstrip('\n')+'\n')
# 3F
scr=f'''{P3}_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, {P3}_OnTransition
	.byte 0

{P3}_OnTransition::
	goto_if_set FLAG_VR_BOSS_DONE, {P3}_EventScript_Done
	end

{P3}_EventScript_Done::
	setvar VAR_TEMP_1, 1
	end

{P3}_EventScript_Red::
	lock
	faceplayer
	goto_if_set FLAG_VR_BOSS_DONE, {P3}_EventScript_RedHeal
	msgbox {P3}_Text_RedSilent
	release
	end

{P3}_EventScript_RedHeal::
	msgbox {P3}_Text_RedHeals
	special HealPlayerParty
	playfanfare MUS_HEAL
	waitfanfare
	msgbox {P3}_Text_RedSilent
	release
	end

{P3}_EventScript_FinalScene::
	lockall
	msgbox {P3}_Text_ShapeA
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	playse SE_THUNDER
	special ShakeScreen
	waitstate
	msgbox {P3}_Text_ShapeB
	closemessage
	fadescreen FADE_TO_BLACK
	delay 60
	fadescreen FADE_FROM_BLACK
	msgbox {P3}_Text_ShapeC
	msgbox {P3}_Text_RedAfter
	closemessage
	setflag FLAG_VR_BOSS_DONE
	setvar VAR_TEMP_1, 1
	releaseall
	end
'''
wr(f'data/maps/{M3}/scripts.inc',scr)
txt=box(P3+'_Text_RedSilent',[["RED: ……"]])+'\n'
txt+=box(P3+'_Text_RedHeals',[["RED takes out a thermos and lets","your POKéMON drink. They feel","fine again."]])+'\n'
txt+=box(P3+'_Text_ShapeA',[["The THRONE ROOM is freezing. RED","kneels at its center, the BLACK"],["OPAL in both hands. Above him","stands a shape made of darkness."]])+'\n'
txt+=box(P3+'_Text_ShapeB',[["It reaches out. The BLACK OPAL","goes dark in RED's palms, then"],["dissolves into the shape.","The ground trembles."],["Seven stones sing below. Three","are still missing. The shape"],["turns its head toward you.","Then everything goes black."]])+'\n'
txt+=box(P3+'_Text_ShapeC',[["When the light returns, the shape","is gone. Only RED remains."]])+'\n'
txt+=box(P3+'_Text_RedAfter',[["RED lowers his head. He did not","win. Nobody could."],["He looks at you, and nods once."]])
wr(f'data/maps/{M3}/text.inc',txt+'\n')

# ---------- VR 2F : ladder to the lair, remove provisional finale, exit blocked ----------
p='data/maps/VictoryRoad_2F/map.json'; m=json.load(open(p))
m['object_events']=[o for o in m['object_events'] if o.get('local_id') not in ('LOCALID_VR_VESPER','LOCALID_VR_RED_2F')]
m['coord_events']=[c for c in m['coord_events'] if c['script']!='VictoryRoad_2F_EventScript_FinalScene']
for (x,y) in ((47,12),(48,11),(49,12)): m['coord_events'].append({"type":"trigger","x":x,"y":y,"elevation":3,"var":"VAR_TEMP_6","var_value":"0","script":"VictoryRoad_2F_EventScript_ExitBlockedN"})
m['coord_events'].append({"type":"trigger","x":47,"y":14,"elevation":3,"var":"VAR_TEMP_6","var_value":"0","script":"VictoryRoad_2F_EventScript_ExitBlockedS"})
m['warp_events'].append({"x":30,"y":1,"elevation":3,"dest_map":"MAP_VICTORY_ROAD_LAIR_1F","dest_warp_id":"0"})
save(p,m)
lay=[l for l in json.load(open('data/layouts/layouts.json'))['layouts'] if l.get('id')=='LAYOUT_VICTORY_ROAD_2F'][0]
w=lay['width']; bp=lay['blockdata_filepath']; d=list(struct.unpack('<%dH'%(w*lay['height']),open(bp,'rb').read()))
d[0*w+30]=(654&0x3ff)|(1<<10)|(0<<12)      # ladder top on the wall (collision)
d[1*w+30]=(662&0x3ff)|(0<<10)|(3<<12)      # ladder warp cell
open(bp,'wb').write(struct.pack('<%dH'%len(d),*d))
sp='data/maps/VictoryRoad_2F/scripts.inc'; s=rd(sp)
a=s.index('VictoryRoad_2F_OnTransition::'); s=s[:a].rstrip('\n')+'\n'
s=s.replace('\tmap_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_2F_OnTransition\n','',1)
s=s.replace('\tmap_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad\n','\tmap_script MAP_SCRIPT_ON_LOAD, VictoryRoad_2F_OnLoad\n\tmap_script MAP_SCRIPT_ON_TRANSITION, VictoryRoad_2F_OnTransition\n',1)
s+='''
VictoryRoad_2F_OnTransition::
	goto_if_set FLAG_VR_BOSS_DONE, VictoryRoad_2F_EventScript_ExitOpen
	end

VictoryRoad_2F_EventScript_ExitOpen::
	setvar VAR_TEMP_6, 1
	end

VictoryRoad_2F_EventScript_ExitBlockedN::
	lockall
	msgbox VictoryRoad_2F_Text_ExitBlocked
	applymovement LOCALID_PLAYER, VictoryRoad_2F_Movement_PushUp
	waitmovement 0
	releaseall
	end

VictoryRoad_2F_EventScript_ExitBlockedS::
	lockall
	msgbox VictoryRoad_2F_Text_ExitBlocked
	applymovement LOCALID_PLAYER, VictoryRoad_2F_Movement_PushDown
	waitmovement 0
	releaseall
	end

VictoryRoad_2F_Movement_PushUp::
	walk_up
	step_end

VictoryRoad_2F_Movement_PushDown::
	walk_down
	step_end
'''
wr(sp,s)
tp='data/maps/VictoryRoad_2F/text.inc'; t=rd(tp)
for lab in ('ShapeA','ShapeB','VesperIntro','VesperDefeat','VesperPost','RedAfter','RedSilent','RedHeals'):
    if 'VictoryRoad_2F_Text_%s::'%lab in t:
        a=t.index('VictoryRoad_2F_Text_%s::'%lab); b=t.find('\n\n',a); b=len(t) if b<0 else b; t=t[:a]+t[b:].lstrip('\n')
t=t.rstrip('\n')+'\n\n'+box('VictoryRoad_2F_Text_ExitBlocked',[["A wall of black mist seals the way","out. Something ancient stirs below"],["the cave. Look for a way down."]])
wr(tp,t+'\n')
print('ok')
