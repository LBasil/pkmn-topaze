#!/usr/bin/env python3
"""Echo 1 : Raikou vit dans le REPAIRE DE L'ORAGE (OneIsland_KindleRoad_StormDen), grotte cachee dans la falaise sud de la route Kindle,
gardee par des acolytes electriques et une oracle. Les 3 etincelles de la route y menent. Copie de la carte MtEmber_RubyPath_B3F. Idempotent (marqueur)."""
import json,re,sys,os,shutil,collections
sys.path[:0]=['docs/topaze','tools/topaze/maps']
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
D='OneIsland_KindleRoad_StormDen'; K='OneIsland_KindleRoad'
if os.path.exists('data/maps/%s/map.json'%D): print('already'); sys.exit(0)
def box(label,boxes):
    out=label+'::\n'
    for bi,bx in enumerate(boxes):
        for li,l in enumerate(bx):
            assert len(l)<=35,(len(l),l)
            ll=li==len(bx)-1; lb=bi==len(boxes)-1
            out+='    .string "'+l+('$' if ll and lb else '\\p' if ll else '\\n')+'"\n'
    return out
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')
# ---- layout (copie de B3F) ----
os.makedirs('data/layouts/'+D,exist_ok=True)
for f in ('map.bin','border.bin'): shutil.copy('data/layouts/MtEmber_RubyPath_B3F/'+f,'data/layouts/%s/%s'%(D,f))
lj=json.load(open('data/layouts/layouts.json')); src=[l for l in lj['layouts'] if l.get('id')=='LAYOUT_MT_EMBER_RUBY_PATH_B3F'][0]
new=dict(src); new['id']='LAYOUT_ONE_ISLAND_KINDLE_ROAD_STORM_DEN'; new['name']=D+'_Layout'
new['border_filepath']='data/layouts/%s/border.bin'%D; new['blockdata_filepath']='data/layouts/%s/map.bin'%D
lj['layouts'].append(new); save('data/layouts/layouts.json',lj)
# ---- entree sur la route Kindle : bouche de grotte (6,124) ----
import mapkit
L=mapkit.Layout('LAYOUT_ONE_ISLAND_KINDLE_ROAD')
i=124*L.w+6; L.g[i]=(L.g[i]&~0x3ff&~(3<<10))|0xa9; L.save()
kj=json.load(open('data/maps/%s/map.json'%K))
kj['object_events']=[o for o in kj['object_events'] if 'RAIKOU' not in o['graphics_id']]
kj['warp_events'].append({"x":6,"y":124,"elevation":0,"dest_map":"MAP_ONE_ISLAND_KINDLE_ROAD_STORM_DEN","dest_warp_id":"0"})
kj['coord_events']=[{"type":"trigger","x":6,"y":125,"elevation":0,"var":"VAR_ECHO_STAGE","var_value":"0","script":K+"_EventScript_DenLockedBill"},
                    {"type":"trigger","x":6,"y":125,"elevation":0,"var":"VAR_ECHO_STAGE","var_value":"1","script":K+"_EventScript_DenLockedSparks"}]
save('data/maps/%s/map.json'%K,kj)
# ---- scripts Kindle : plus de Raikou sur la route ----
s=rd('data/maps/%s/scripts.inc'%K)
a=s.index('OneIsland_KindleRoad_EventScript_TransSpark3::'); b=s.index('OneIsland_KindleRoad_EventScript_ShowSpark3::')
s=s[:a]+'OneIsland_KindleRoad_EventScript_TransSpark3::\n\tgoto_if_unset FLAG_ECHO1_SPARK_DONE3, OneIsland_KindleRoad_EventScript_ShowSpark3\n\tend\n\n'+s[b:]
s=s.replace("""	setflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_EchoSpark1""","""	end

OneIsland_KindleRoad_EventScript_EchoSpark1""",1)
s=s.replace("""	clearflag FLAG_HIDE_ECHO_BEAST
	setobjectxyperm LOCALID_ONE_ISLAND_RAIKOU, 16, 132
	addobject LOCALID_ONE_ISLAND_RAIKOU
""","",1)
s+=f"""
@ Topaze: la bouche de grotte du repaire (6,124) reste fermee tant que Bill et les etincelles n'ont pas parle
{K}_EventScript_DenLockedBill::
	lockall
	msgbox {K}_Text_DenLockedBill
	applymovement LOCALID_PLAYER, {K}_Movement_DenBack
	waitmovement 0
	releaseall
	end

{K}_EventScript_DenLockedSparks::
	goto_if_set FLAG_ECHO1_SPARK_DONE3, EventScript_Return
	lockall
	msgbox {K}_Text_DenLockedSparks
	applymovement LOCALID_PLAYER, {K}_Movement_DenBack
	waitmovement 0
	releaseall
	end

{K}_Movement_DenBack::
	walk_down
	step_end
"""
wr('data/maps/%s/scripts.inc'%K,s)
t=rd('data/maps/%s/text.inc'%K)
t=re.sub(r'OneIsland_KindleRoad_Text_EchoSpark3b::.*?\$"\n','OneIsland_KindleRoad_Text_EchoSpark3b::\n    .string "The sparks gather in the south\\\\n"\n    .string "cliff and sink into a CAVE.\\\\p"\n    .string "Whatever hides inside keeps\\\\n"\n    .string "the storm alive.$"\n',t,flags=re.S)
t+="\n"+box(K+'_Text_DenLockedBill',[["A cave mouth hums with static.","Something forbids the way."]])+"\n"+box(K+'_Text_DenLockedSparks',[["Static crawls over the rock.","The cave is not ready for you."],["Follow the ECHO sparks first."]])
wr('data/maps/%s/text.inc'%K,t)
# ---- carte du repaire ----
mj=json.load(open('data/maps/MtEmber_RubyPath_B3F/map.json'))
mj['id']='MAP_ONE_ISLAND_KINDLE_ROAD_STORM_DEN'; mj['name']=D; mj['layout']='LAYOUT_ONE_ISLAND_KINDLE_ROAD_STORM_DEN'; mj['region_map_section']='MAPSEC_ONE_ISLAND'
mj['weather']='WEATHER_NONE'; mj['connections']=None
mj['warp_events']=[{"x":x,"y":y,"elevation":0,"dest_map":"MAP_ONE_ISLAND_KINDLE_ROAD","dest_warp_id":"3"} for (x,y) in ((19,19),(1,4),(5,19))]
mj['coord_events']=[]; mj['bg_events']=[]
import route_test as R
R.SURF=False
nv=R.Nav('MtEmber_RubyPath_B3F'); nv.objs=set()
st=(19,19); par={st:None}; q=collections.deque([st])
while q:
    c=q.popleft()
    for dx,dy in((0,1),(0,-1),(1,0),(-1,0)):
        m=(c[0]+dx,c[1]+dy)
        if m in par or nv.blocked(*m) or not nv.step_ok(c,m): continue
        par[m]=c; q.append(m)
path=[]; c=(1,4)
while c: path.append(c); c=par[c]
path.reverse()
def face(i):
    a,b=path[i],path[i-1]; return {(0,1):'DOWN',(0,-1):'UP',(1,0):'RIGHT',(-1,0):'LEFT'}[(b[0]-a[0],b[1]-a[1])]
def trn(gfx,i,script,sight):
    x,y=path[i]; return {"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_"+face(i),"movement_range_x":0,"movement_range_y":0,
      "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":str(sight),"script":script,"flag":"0"}
# (cle, slot RS_, gfx, nom, equipe, intro, defaite, apres)
G=[('Acolyte1','RS_PKMN_RANGER_M','OBJ_EVENT_GFX_CHANNELER','SPARK',[('RAICHU',62),('ELECTRODE',62),('MAGNETON',63)],
    [["Another seeker of the beast?","The STORM does not like visitors."]],["Your storm is stronger..."],[["The beast sleeps at the end of","the cave. Many guard its sleep."]]),
   ('Acolyte2','RS_PKMN_RANGER_F','OBJ_EVENT_GFX_CHANNELER','VOLT',[('ELECTABUZZ',63),('AMPHAROS',63),('JOLTEON',63)],
    [["We keep the thunder company.","You are only noise."]],["Quiet at last."],[["Follow the humming. It grows."]]),
   ('Acolyte3','RS_BIRD_KEEPER','OBJ_EVENT_GFX_BLACK_BELT','AMP',[('MANECTRIC',64),('ELECTRODE',64),('RAICHU',64),('RHYDON',64)],
    [["The beast gave us light when the","world went dark. We repay it."]],["The light forgives you."],[["Only the ORACLE can open the","last gate."]]),
   ('Acolyte4','RS_SWIMMER_M','OBJ_EVENT_GFX_FAT_MAN','OHM',[('AMPHAROS',65),('ELECTABUZZ',65),('MAGNETON',65),('MANECTRIC',65)],
    [["Turn back, runner! This cave is","a temple, not a playground!"]],["The temple is quiet again."],[["The ORACLE heard you coming."]]),
   ('Oracle','RS_SWIMMER_F','OBJ_EVENT_GFX_OLD_WOMAN','ORACLE',[('MAGNETON',66),('RAICHU',66),('ELECTRODE',66),('JOLTEON',67),('MANECTRIC',67),('AMPHAROS',68)],
    [["I am the ORACLE of the STORM.","Since the ECHO opened, the beast"],["has slept in our hall, and we","have kept it safe."]],["...Then the storm has chosen you."],[["Go. But treat it as the storm","treats us: with respect."]])]
# ---- dresseurs ----
tr=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
for k,tid,gfx,name,team,a,b,c in G:
    bb=re.search(r'\[TRAINER_%s\] = \{.*?\n    \},'%tid,tr,re.S).group(0)
    nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_CHANNELER',bb)
    nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_SUSPICIOUS',nb)
    nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_%s'%('PSYCHIC_F' if k=='Oracle' else 'CHANNELER'),nb)
    nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("%s")'%name,nb)
    nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY' if k=='Oracle' else 'AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT',nb)
    sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
    nb=re.sub(r'(?:NO_)?ITEM_(?:DEFAULT|CUSTOM)_MOVES\(','NO_ITEM_DEFAULT_MOVES(',nb)
    tr=tr.replace(bb,nb)
    m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S); assert m,sym
    body=''.join('    {\n        .iv = %d,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(60 if k=='Oracle' else 40,lv,sp) for sp,lv in team)
    pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',tr); wr('src/data/trainer_parties.h',pa)
# ---- objets de la carte ----
objs=[]; idxs=[12,21,29,37,44]
for (k,tid,gfx,name,team,a,b,c),i in zip(G,idxs): objs.append(trn(gfx,i,'%s_EventScript_%s'%(D,k),0 if False else 4))
rx,ry=3,4
objs.append({"local_id":"LOCALID_STORM_DEN_RAIKOU","type":"object","graphics_id":"OBJ_EVENT_GFX_RAIKOU","x":rx,"y":ry,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_RIGHT","movement_range_x":0,"movement_range_y":0,
   "trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":D+"_EventScript_Raikou","flag":"FLAG_HIDE_ECHO_BEAST"})
mj['object_events']=objs; os.makedirs('data/maps/'+D,exist_ok=True); save('data/maps/%s/map.json'%D,mj)
print('positions',[(path[i],face(i)) for i in idxs],'raikou',(rx,ry))
# ---- scripts / textes ----
scr=f"""{D}_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, {D}_OnTransition
	.byte 0

{D}_OnTransition::
	goto_if_set FLAG_ECHO_BEAST_DONE, {D}_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 1, {D}_EventScript_HideBeast
	clearflag FLAG_HIDE_ECHO_BEAST
	end

{D}_EventScript_HideBeast::
	setflag FLAG_HIDE_ECHO_BEAST
	end
"""
txt=''
for k,tid,gfx,name,team,a,b,c in G:
    scr+=f'\n{D}_EventScript_{k}::\n\ttrainerbattle_single TRAINER_{tid}, {D}_Text_{k}Intro, {D}_Text_{k}Defeat\n\tmsgbox {D}_Text_{k}Post, MSGBOX_AUTOCLOSE\n\tend\n'
    txt+=box(f'{D}_Text_{k}Intro',a)+'\n'+box(f'{D}_Text_{k}Defeat',[b])+'\n'+box(f'{D}_Text_{k}Post',c)+'\n'
scr+=f"""
@ Topaze: Raikou (Echo 1), tapi au fond de la grotte
{D}_EventScript_Raikou::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_RAIKOU, 0
	waitse
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {D}_EventScript_DefeatedRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {D}_EventScript_RanFromRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {D}_EventScript_RanFromRaikou
	setflag FLAG_ECHO_BEAST_DONE
	setflag FLAG_HIDE_ECHO_BEAST
	setvar VAR_ECHO_STAGE, 2
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone1
	end

{D}_EventScript_DefeatedRaikou::
	setflag FLAG_ECHO_BEAST_DONE
	setvar VAR_ECHO_STAGE, 2
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone1
	end

{D}_EventScript_RanFromRaikou::
	setvar VAR_0x8004, SPECIES_RAIKOU
	goto EventScript_MonFlewAway
	end
"""
wr(f'data/maps/{D}/scripts.inc',scr); wr(f'data/maps/{D}/text.inc',txt.rstrip('\n')+'\n')
# ---- enregistrement ----
j=json.load(open('data/maps/map_groups.json'))
if D not in j['gMapGroup_Dungeons']: j['gMapGroup_Dungeons'].append(D)
save('data/maps/map_groups.json',j)
f='data/event_scripts.s'; s=rd(f)
for kind in ('scripts','text'):
    anchor='\t.include "data/maps/%s/%s.inc"\n'%(K,kind); assert anchor in s
    s=s.replace(anchor,anchor+'\t.include "data/maps/%s/%s.inc"\n'%(D,kind),1)
wr(f,s)
print('ok')
