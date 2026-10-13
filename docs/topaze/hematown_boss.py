#!/usr/bin/env python3
"""Hematown stage 2: the allies (BRICE, FLORA, N) enter the HEMATEK tower, the unseen boss crushes them,
KRONOS is fought by the player, the HEMATITE is stolen. Run once from repo root (idempotent via marker)."""
import json,re,sys
MARK='FLAG_HEMATEK_ALLIES_IN'
if MARK in open('include/constants/flags.h').read() and 'AlliesMeet' in open('data/maps/SaffronCity/scripts.inc').read():
    print('already applied'); sys.exit(0)

def rd(p): return open(p).read()
def wr(p,s): open(p,'w').write(s)
def sub(p,old,new):
    s=rd(p); assert old in s,(p,old[:50]); wr(p,s.replace(old,new,1))
def check_text(s):
    for l in re.findall(r'\.string "(.*)"',s):
        t=re.sub(r'\{[^}]*\}','XXXXXXXX' if False else 'X',l); t=re.sub(r'\\[nlp$]','',t).replace('$','')
        for seg in re.split(r'\\n|\\p|\\l',l.rstrip('$')):
            seg2=re.sub(r'\{[^}]*\}','X',seg)
            assert len(seg2)<=35,(len(seg2),seg2)
def addtext(p,s):
    check_text(s); wr(p,rd(p).rstrip('\n')+'\n\n'+s.strip('\n')+'\n')
def obj(local,gfx,x,y,script,flag,elev=3,move='MOVEMENT_TYPE_FACE_DOWN'):
    return {"local_id":local,"type":"object","graphics_id":gfx,"x":x,"y":y,"elevation":elev,"movement_type":move,
            "movement_range_x":1,"movement_range_y":1,"trainer_type":"TRAINER_TYPE_NONE",
            "trainer_sight_or_berry_tree_id":"0","script":script,"flag":flag}
def mj(name):
    p=f'data/maps/{name}/map.json'; return p,json.load(open(p))
def save(p,m): json.dump(m,open(p,'w'),indent=2); open(p,'a').write('\n')

# ---------- flags ----------
f='include/constants/flags.h'
sub(f,'#define FLAG_0x077                                         0x077','#define FLAG_HEMATEK_ALLIES_IN                             0x077')
sub(f,'#define FLAG_0x078                                         0x078','#define FLAG_HEMATEK_BOSS_DONE                             0x078')
sub(f,'#define FLAG_0x0AF               0x0AF','#define FLAG_HEMATEK_BRICE_GONE  0x0AF')
sub(f,'#define FLAG_0x0B0               0x0B0','#define FLAG_HEMATEK_FLORA_GONE  0x0B0')
sub(f,'#define FLAG_0x0B1               0x0B1','#define FLAG_HEMATEK_N_GONE      0x0B1')
sub(f,'#define FLAG_HEMATITE_GIVEN      0x027','#define FLAG_HEMATITE_STOLEN     0x027')

GFX={'BRICE':'OBJ_EVENT_GFX_BRUNO','FLORA':'OBJ_EVENT_GFX_ERIKA','N':'OBJ_EVENT_GFX_LANCE'}

# ---------- tower: remove elevator warps + 11F door ----------
for n in range(1,12):
    p,m=mj(f'SilphCo_{n}F'); m['warp_events']=[w for w in m['warp_events'] if 'ELEVATOR' not in w['dest_map']]; save(p,m)
s=rd('data/maps/SilphCo_11F/scripts.inc')
s=s.replace('\tcall_if_unset FLAG_SILPH_11F_DOOR, EventScript_Close11FDoor\n','')
wr('data/maps/SilphCo_11F/scripts.inc',s)

# ---------- SaffronCity (Hematown): meeting scene ----------
p,m=mj('SaffronCity')
for loc,key,x in (('LOCALID_HEMATOWN_BRICE','BRICE',33),('LOCALID_HEMATOWN_FLORA','FLORA',32),('LOCALID_HEMATOWN_N','N',35)):
    m['object_events'].append(obj(loc,GFX[key],x,37,'SaffronCity_EventScript_AllyStub','FLAG_TEMP_%d'%{'BRICE':1,'FLORA':2,'N':3}[key],move='MOVEMENT_TYPE_FACE_UP'))
m['coord_events'].append({"type":"trigger","x":33,"y":32,"elevation":3,"var":"VAR_TEMP_1","var_value":"0","script":"SaffronCity_EventScript_AlliesMeet"})
save(p,m)
sp='data/maps/SaffronCity/scripts.inc'
sub(sp,'\tsetworldmapflag FLAG_WORLD_MAP_SAFFRON_CITY\n','\tsetworldmapflag FLAG_WORLD_MAP_SAFFRON_CITY\n\tsetflag FLAG_TEMP_1\n\tsetflag FLAG_TEMP_2\n\tsetflag FLAG_TEMP_3\n')
sub(sp,'''SaffronCity_EventScript_DoorGuardGrunt::
	lock
''','''SaffronCity_EventScript_AllyStub::
	end

SaffronCity_EventScript_AlliesMeet::
	lockall
	setvar VAR_TEMP_1, 1
	goto_if_set FLAG_HEMATEK_ALLIES_IN, SaffronCity_EventScript_AlliesMeetEnd
	playse SE_PIN
	applymovement LOCALID_PLAYER, Common_Movement_ExclamationMark
	waitmovement 0
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_2
	clearflag FLAG_TEMP_3
	addobject LOCALID_HEMATOWN_BRICE
	addobject LOCALID_HEMATOWN_FLORA
	addobject LOCALID_HEMATOWN_N
	applymovement LOCALID_PLAYER, Common_Movement_WalkInPlaceFasterDown
	applymovement LOCALID_HEMATOWN_BRICE, SaffronCity_Movement_BriceComes
	applymovement LOCALID_HEMATOWN_FLORA, SaffronCity_Movement_FloraComes
	applymovement LOCALID_HEMATOWN_N, SaffronCity_Movement_NComes
	waitmovement 0
	msgbox SaffronCity_Text_AlliesMeet1
	msgbox SaffronCity_Text_AlliesMeet2
	msgbox SaffronCity_Text_AlliesMeet3
	msgbox SaffronCity_Text_AlliesMeet4
	closemessage
	applymovement LOCALID_PLAYER, SaffronCity_Movement_PlayerAside
	waitmovement 0
	applymovement LOCALID_HEMATOWN_BRICE, SaffronCity_Movement_BriceEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_BRICE
	applymovement LOCALID_HEMATOWN_FLORA, SaffronCity_Movement_FloraEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_FLORA
	applymovement LOCALID_HEMATOWN_N, SaffronCity_Movement_NEnters
	waitmovement 0
	removeobject LOCALID_HEMATOWN_N
	setflag FLAG_HEMATEK_ALLIES_IN
	releaseall
	end

SaffronCity_EventScript_AlliesMeetEnd::
	releaseall
	end

SaffronCity_Movement_BriceComes::
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_FloraComes::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_NComes::
	walk_up
	walk_up
	walk_up
	walk_up
	walk_up
	step_end

SaffronCity_Movement_PlayerAside::
	walk_left
	step_end

SaffronCity_Movement_BriceEnters::
	walk_up
	walk_up
	step_end

SaffronCity_Movement_FloraEnters::
	walk_right
	walk_up
	walk_up
	step_end

SaffronCity_Movement_NEnters::
	walk_left
	walk_left
	walk_up
	walk_up
	step_end

SaffronCity_EventScript_DoorGuardGrunt::
	lock
	goto_if_set FLAG_HEMATEK_BOSS_DONE, SaffronCity_EventScript_DoorGuardGone
	goto_if_set FLAG_HEMATEK_ALLIES_IN, SaffronCity_EventScript_DoorGuardScared
''')
sub(sp,'SaffronCity_EventScript_DoorGuardAsleep::','''SaffronCity_EventScript_DoorGuardScared::
	msgbox SaffronCity_Text_GuardScared
	release
	end

SaffronCity_EventScript_DoorGuardGone::
	msgbox SaffronCity_Text_GuardGone
	release
	end

SaffronCity_EventScript_DoorGuardAsleep::''')
addtext('data/maps/SaffronCity/text.inc','''
SaffronCity_Text_AlliesMeet1::
    .string "N: …Wait. Do not go in, child.\\p"
    .string "That pendant. It hums like the\\n"
    .string "stones. So it is true.$"

SaffronCity_Text_AlliesMeet2::
    .string "BRICE: I'm BRICE. I walked this\\n"
    .string "region long before ONYBRIS.\\p"
    .string "Their MASTER is in this tower.\\n"
    .string "He came for the HEMATITE himself.$"

SaffronCity_Text_AlliesMeet3::
    .string "FLORA: We are going up to face\\n"
    .string "him. Every trainer that can still\\p"
    .string "stand has to try.\\p"
    .string "You are not strong enough yet,\\n"
    .string "little one. Not for him.$"

SaffronCity_Text_AlliesMeet4::
    .string "N: Follow us if you must.\\n"
    .string "Stay one floor behind.\\p"
    .string "And {PLAYER}… if we do not come\\n"
    .string "down, remember what you saw.$"

SaffronCity_Text_GuardScared::
    .string "I didn't see anything!\\n"
    .string "Those three… I'm not paid enough!$"

SaffronCity_Text_GuardGone::
    .string "The MASTER is gone. Half of us\\n"
    .string "ran. I think I'll quit too.$"
''')

# ---------- floors: allies stationed 3F/6F/9F ----------
import collections,struct
dl=json.load(open('data/layouts/layouts.json'))['layouts']
def grid(layout):
    l=[x for x in dl if x.get('id')==layout][0]; w,h=l['width'],l['height']; b=open(l['blockdata_filepath'],'rb').read()
    return w,h,[[ (struct.unpack_from('<H',b,(y*w+x)*2)[0]>>10)&3 for x in range(w)] for y in range(h)]
def path_moves(name,start,goal,blocked):
    p,m=mj(name); w,h,g=grid(m['layout']); W={(k['x'],k['y']) for k in m['warp_events']}
    prev={start:None};q=collections.deque([start])
    while q:
        c=q.popleft()
        if c==goal: break
        for dx,dy in((1,0),(-1,0),(0,1),(0,-1)):
            n=(c[0]+dx,c[1]+dy)
            if 0<=n[0]<w and 0<=n[1]<h and n not in prev and n not in blocked and (g[n[1]][n[0]]==0 or n==goal):
                prev[n]=c;q.append(n)
    path=[goal]
    while prev[path[-1]] is not None: path.append(prev[path[-1]])
    path=path[::-1]; names={(1,0):'right',(-1,0):'left',(0,1):'down',(0,-1):'up'}
    return ['walk_'+names[(b[0]-a[0],b[1]-a[1])] for a,b in zip(path,path[1:])]
def mktext(label,boxes):
    """boxes: list of boxes; each box = list of lines (<=2). Returns .string block."""
    out=label+'::\n'
    for bi,box in enumerate(boxes):
        for li,l in enumerate(box):
            last_line=(li==len(box)-1); last_box=(bi==len(boxes)-1)
            sep='$' if (last_line and last_box) else ('\\p' if last_line else '\\n')
            out+='    .string "'+l+sep+'"\n'
    return out

ALLY=[(3,'BRICE',(29,4),'FLAG_HEMATEK_BRICE_GONE',
 [["BRICE: Careful. The goons on this","floor are small fry."],
  ["The ones above are real fighters.","I will hold the stairs for you."],
  ["FLORA is ahead of us, N higher","still. Do not rush, kid."]]),
 (6,'FLORA',(25,5),'FLAG_HEMATEK_FLORA_GONE',
 [["FLORA: Oh. You came after all."],
  ["These POKéMON are not evil.","They were just told to be."],
  ["Please be gentle with them.","I must go. He does not wait."]]),
 (9,'N',(17,4),'FLAG_HEMATEK_N_GONE',
 [["N: I can hear their POKéMON.","They are afraid of him."],
  ["Not of us. Of HIM."],
  ["Stay here a moment, {PLAYER}.","Some doors should be opened by"],
  ["those who can survive behind them."]])]
for fl,key,(x,y),gone,boxes in ALLY:
    name=f'SilphCo_{fl}F'; p,m=mj(name)
    loc=f'LOCALID_SILPH_CO_{fl}F_{key}'
    m['object_events'].append(obj(loc,GFX[key],x,y,f'{name}_EventScript_Ally','FLAG_TEMP_1'))
    up=[w for w in m['warp_events'] if w['dest_map']==f'MAP_SILPH_CO_{fl+1}F'][0]
    blocked={(o['x'],o['y']) for o in m['object_events']}-{(x,y)}
    moves=path_moves(name,(x,y),(up['x'],up['y']),blocked)
    save(p,m)
    sp=f'data/maps/{name}/scripts.inc'; s=rd(sp)
    assert 'MAP_SCRIPT_ON_TRANSITION' not in s
    s=s.replace('\t.byte 0\n','\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransition\n\t.byte 0\n'%name,1)
    s+=f'''
{name}_OnTransition::
	goto_if_unset FLAG_HEMATEK_ALLIES_IN, {name}_EventScript_HideAlly
	goto_if_set FLAG_HEMATEK_BOSS_DONE, {name}_EventScript_HideAlly
	goto_if_set {gone}, {name}_EventScript_HideAlly
	end

{name}_EventScript_HideAlly::
	setflag FLAG_TEMP_1
	end

{name}_EventScript_Ally::
	lock
	faceplayer
	msgbox {name}_Text_Ally
	closemessage
	applymovement {loc}, {name}_Movement_AllyLeaves
	waitmovement 0
	removeobject {loc}
	setflag {gone}
	release
	end

{name}_Movement_AllyLeaves::
'''+''.join(f'\t{mv}\n' for mv in moves)+'\tstep_end\n'
    wr(sp,s)
    addtext(f'data/maps/{name}/text.inc',mktext(f'{name}_Text_Ally',boxes))

# ---------- 11F: Kronos + boss cutscene ----------
p,m=mj('SilphCo_11F')
for loc,key,x,t in (('LOCALID_SILPH_CO_11F_BRICE','BRICE',8,1),('LOCALID_SILPH_CO_11F_FLORA','FLORA',9,2),('LOCALID_SILPH_CO_11F_N','N',10,3)):
    m['object_events'].append(obj(loc,GFX[key],x,14,'SilphCo_11F_EventScript_Ally'+key.title(),f'FLAG_TEMP_{t}'))
save(p,m)
sp='data/maps/SilphCo_11F/scripts.inc'; s=rd(sp)
s=s.replace('''	map_script MAP_SCRIPT_ON_LOAD, SilphCo_11F_OnLoad
	.byte 0
''','''	map_script MAP_SCRIPT_ON_LOAD, SilphCo_11F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SilphCo_11F_OnTransition
	.byte 0

SilphCo_11F_OnTransition::
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	end

SilphCo_11F_EventScript_AllyBrice::
	msgbox SilphCo_11F_Text_AfterBrice, MSGBOX_NPC
	end

SilphCo_11F_EventScript_AllyFlora::
	msgbox SilphCo_11F_Text_AfterFlora, MSGBOX_NPC
	end

SilphCo_11F_EventScript_AllyN::
	msgbox SilphCo_11F_Text_AfterN, MSGBOX_NPC
	end
''',1)
old=s[s.index('SilphCo_11F_EventScript_BattleGiovanni::'):s.index('SilphCo_11F_EventScript_GiovanniApproachLeft::')]
new='''SilphCo_11F_EventScript_BattleGiovanni::
	textcolor NPC_TEXT_COLOR_MALE
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 2
	setvar VAR_0x8006, 6
	setvar VAR_0x8007, 3
	playse SE_M_EXPLOSION
	special ShakeScreen
	waitstate
	msgbox SilphCo_11F_Text_MuffledCrash
	applymovement LOCALID_SILPH_CO_GIOVANNI, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	delay 25
	msgbox SilphCo_11F_Text_GiovanniIntro
	closemessage
	call_if_eq VAR_TEMP_1, 0, SilphCo_11F_EventScript_GiovanniApproachLeft
	call_if_eq VAR_TEMP_1, 1, SilphCo_11F_EventScript_GiovanniApproachRight
	setvar VAR_LAST_TALKED, LOCALID_SILPH_CO_GIOVANNI
	trainerbattle_no_intro TRAINER_BOSS_GIOVANNI_2, SilphCo_11F_Text_GiovanniDefeat
	msgbox SilphCo_11F_Text_GiovanniPostBattle
	closemessage
	setvar VAR_0x8004, 1
	setvar VAR_0x8005, 3
	setvar VAR_0x8006, 8
	setvar VAR_0x8007, 4
	playse SE_THUNDER
	special ShakeScreen
	waitstate
	playse SE_M_EXPLOSION
	special ShakeScreen
	waitstate
	fadescreen FADE_TO_BLACK
	removeobject LOCALID_SILPH_CO_GIOVANNI
	removeobject LOCALID_SILPH_CO_11F_GRUNT1
	removeobject LOCALID_SILPH_CO_11F_GRUNT2
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_2
	clearflag FLAG_TEMP_3
	addobject LOCALID_SILPH_CO_11F_BRICE
	addobject LOCALID_SILPH_CO_11F_FLORA
	addobject LOCALID_SILPH_CO_11F_N
	fadescreen FADE_FROM_BLACK
	msgbox SilphCo_11F_Text_ShadowPasses
	msgbox SilphCo_11F_Text_BossBrice
	msgbox SilphCo_11F_Text_BossFlora
	msgbox SilphCo_11F_Text_BossN
	closemessage
	setvar VAR_MAP_SCENE_SILPH_CO_11F, 1
	setflag FLAG_HEMATEK_BOSS_DONE
	setflag FLAG_HEMATITE_STOLEN
	setflag FLAG_HIDE_SAFFRON_ROCKETS
	clearflag FLAG_HIDE_SAFFRON_CIVILIANS
	releaseall
	end

'''
s=s.replace(old,new,1); wr(sp,s)
# rewrite Kronos texts + add scene texts
tp='data/maps/SilphCo_11F/text.inc'; t=rd(tp)
a=t.index('SilphCo_11F_Text_GiovanniIntro::'); b=t.index('SilphCo_11F_Text_Grunt2Intro::')
newk=mktext('SilphCo_11F_Text_GiovanniIntro',[
 ["KRONOS: You again, child.","I warned you once."],
 ["BRICE, FLORA, N… the old heroes","of KANTO went in to face the"],
 ["MASTER. They will not come out","standing."],
 ["Run home. Or pay for staying!"]])+'\n'+mktext('SilphCo_11F_Text_GiovanniDefeat',[
 ["Hmph…","You are stronger than you look."]])+'\n'+mktext('SilphCo_11F_Text_GiovanniPostBattle',[
 ["KRONOS: Good. Strong enough to","watch. Not strong enough to"],
 ["stand against him."],
 ["Listen. That sound is the end of","the old heroes."]])+'\n'
check_text(newk)
t=t[:a]+newk+t[b:]
wr(tp,t)
addtext(tp,mktext('SilphCo_11F_Text_MuffledCrash',[["A crash shakes the floor.","It came from behind the doors!"]])
+'\n'+mktext('SilphCo_11F_Text_ShadowPasses',[
 ["…The lights flicker. A black shape","glides past the windows."],
 ["Then it is gone. Only silence."]])
+'\n'+mktext('SilphCo_11F_Text_BossBrice',[
 ["BRICE: …Not even a scratch on him.","One POKéMON. He only used one."],
 ["He took the HEMATITE and walked","out like we were furniture."]])
+'\n'+mktext('SilphCo_11F_Text_BossFlora',[
 ["FLORA: He knew you were here,","{PLAYER}. He looked right at you."],
 ["He said you would find him.","When you are ready."]])
+'\n'+mktext('SilphCo_11F_Text_BossN',[
 ["N: I heard his POKéMON. They are","not afraid. They are empty."],
 ["Get stronger, {PLAYER}. We could","not stop him. Maybe you can."]])
+'\n'+mktext('SilphCo_11F_Text_AfterBrice',[["BRICE: Go. We will live. Barely.","Check on NOX in the gym."]])
+'\n'+mktext('SilphCo_11F_Text_AfterFlora',[["FLORA: I am fine, really.","Look after yourself first."]])
+'\n'+mktext('SilphCo_11F_Text_AfterN',[["N: He took the stone. But he","left something behind: a warning."]]))

# ---------- Pokemon Center 1F ----------
p,m=mj('SaffronCity_PokemonCenter_1F')
for loc,key,x,t in (('LOCALID_HEMATOWN_PC_BRICE','BRICE',12,1),('LOCALID_HEMATOWN_PC_FLORA','FLORA',13,2),('LOCALID_HEMATOWN_PC_N','N',14,3)):
    m['object_events'].append(obj(loc,GFX[key],x,3,'SaffronCity_PokemonCenter_1F_EventScript_Ally'+key.title(),f'FLAG_TEMP_{t}'))
save(p,m)
sp='data/maps/SaffronCity_PokemonCenter_1F/scripts.inc'
sub(sp,'''	setrespawn HEAL_LOCATION_SAFFRON_CITY
	end
''','''	setrespawn HEAL_LOCATION_SAFFRON_CITY
	call_if_unset FLAG_HEMATEK_BOSS_DONE, SaffronCity_PokemonCenter_1F_EventScript_HideAllies
	end

SaffronCity_PokemonCenter_1F_EventScript_HideAllies::
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	return

SaffronCity_PokemonCenter_1F_EventScript_AllyBrice::
	msgbox SaffronCity_PokemonCenter_1F_Text_Brice, MSGBOX_NPC
	end

SaffronCity_PokemonCenter_1F_EventScript_AllyFlora::
	msgbox SaffronCity_PokemonCenter_1F_Text_Flora, MSGBOX_NPC
	end

SaffronCity_PokemonCenter_1F_EventScript_AllyN::
	msgbox SaffronCity_PokemonCenter_1F_Text_N, MSGBOX_NPC
	end
''')
tp='data/maps/SaffronCity_PokemonCenter_1F/text.inc'
addtext(tp,mktext('SaffronCity_PokemonCenter_1F_Text_Brice',[
 ["BRICE: The nurse says we'll walk","again by tomorrow."],
 ["I'm going back to the mountains.","Maybe there I'll think of a plan."]])
+'\n'+mktext('SaffronCity_PokemonCenter_1F_Text_Flora',[
 ["FLORA: He wants all ten stones.","That is what the MASTER said."],
 ["You carry more of them than he","does. Keep them close."]])
+'\n'+mktext('SaffronCity_PokemonCenter_1F_Text_N',[
 ["N: They say two travelers are","already near the volcano."],
 ["Old friends of the road. Meet","them. Learn from them."]]))

# ---------- Gym ----------
gp='data/maps/SaffronCity_Gym/scripts.inc'
sub(gp,'goto_if_unset FLAG_HIDE_SILPH_ROCKETS, SaffronCity_Gym_EventScript_SabrinaBusy','goto_if_unset FLAG_HEMATEK_BOSS_DONE, SaffronCity_Gym_EventScript_SabrinaBusy')
sub(gp,'	goto_if_unset FLAG_HEMATITE_GIVEN, SaffronCity_Gym_EventScript_StoneGift\n','')
sub(gp,'''	msgbox SaffronCity_Gym_Text_StoneGift
	playfanfare MUS_OBTAIN_KEY_ITEM
	message SaffronCity_Gym_Text_ObtainedHematite
	waitmessage
	waitfanfare
	setflag FLAG_HEMATITE_GIVEN
	release''','''	msgbox SaffronCity_Gym_Text_StoneGift
	release''')
gt='data/maps/SaffronCity_Gym/text.inc'; t=rd(gt)
a=t.index('SaffronCity_Gym_Text_SabrinaBusy::')
t=t[:a].rstrip('\n')+'\n\n'+mktext('SaffronCity_Gym_Text_SabrinaBusy',[
 ["NOX: Not now, child."],
 ["Three of the strongest trainers","went into the tower."],
 ["Wait for them to come back,","or not. Then we talk."]])+'\n'+mktext('SaffronCity_Gym_Text_StoneGift',[
 ["NOX: The HEMATITE is gone. He","took it before I could hide it."],
 ["But you have the others. He needs","them all. Make him wait."],
 ["Go south. By sea. The next gate","is a city of lightning."]])
check_text(t); wr(gt,t)
print('applied')
