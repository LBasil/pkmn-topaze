#!/usr/bin/env python3
"""Echo 1 : Raikou n'apparait qu'apres avoir suivi 3 etincelles (Voltorb crepitants) le long de la route Kindle. Idempotent."""
import json,re
S=open('include/constants/flags.h').read()
if 'FLAG_ECHO1_SPARK_DONE1' not in S:
    for n,(a,b) in enumerate((('0x130','FLAG_ECHO1_SPARK_DONE1'),('0x131','FLAG_ECHO1_SPARK_DONE2'),('0x132','FLAG_ECHO1_SPARK_DONE3'),('0x133','FLAG_HIDE_ECHO1_SPARK1'),('0x134','FLAG_HIDE_ECHO1_SPARK2'),('0x135','FLAG_HIDE_ECHO1_SPARK3'))):
        old='#define FLAG_%s'%a
        m=re.search(r'#define FLAG_%s\s+%s\s*\n'%(a,a),S); assert m,a
        S=S.replace(m.group(0),'#define %s %s // Topaze: Echo 1 etincelles\n'%(b,a),1)
    open('include/constants/flags.h','w').write(S)
p='data/maps/OneIsland_KindleRoad/map.json'; d=json.load(open(p))
if not any(o.get('script','').endswith('EchoSpark1') for o in d['object_events']):
    for o in d['object_events']:
        if 'RAIKOU' in o['graphics_id']: o['local_id']='LOCALID_ONE_ISLAND_RAIKOU'
    for i,(x,y) in enumerate(((11,61),(11,81),(11,101)),1):
        d['object_events'].append({"graphics_id":"OBJ_EVENT_GFX_VOLTORB","x":x,"y":y,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,"trainer_type":"TRAINER_TYPE_NONE","trainer_sight_or_berry_tree_id":"0","script":"OneIsland_KindleRoad_EventScript_EchoSpark%d"%i,"flag":"FLAG_HIDE_ECHO1_SPARK%d"%i})
    json.dump(d,open(p,'w'),indent=2); open(p,'a').write('\n')
sp='data/maps/OneIsland_KindleRoad/scripts.inc'; s=open(sp).read()
if 'EchoSpark1' not in s:
    s=s.replace("""OneIsland_KindleRoad_OnTransition::
	goto_if_set FLAG_ECHO_BEAST_DONE, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 1, OneIsland_KindleRoad_EventScript_HideBeast
	clearflag FLAG_HIDE_ECHO_BEAST
	end
""","""OneIsland_KindleRoad_OnTransition::
	@ Topaze: etincelles visibles seulement a l'etape 1 ; Raikou apres les trois
	setflag FLAG_HIDE_ECHO1_SPARK1
	setflag FLAG_HIDE_ECHO1_SPARK2
	setflag FLAG_HIDE_ECHO1_SPARK3
	goto_if_set FLAG_ECHO_BEAST_DONE, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 1, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_unset FLAG_ECHO1_SPARK_DONE1, OneIsland_KindleRoad_EventScript_ShowSpark1
	goto OneIsland_KindleRoad_EventScript_TransSpark2

OneIsland_KindleRoad_EventScript_ShowSpark1::
	clearflag FLAG_HIDE_ECHO1_SPARK1
	goto OneIsland_KindleRoad_EventScript_TransSpark2

OneIsland_KindleRoad_EventScript_TransSpark2::
	goto_if_unset FLAG_ECHO1_SPARK_DONE2, OneIsland_KindleRoad_EventScript_ShowSpark2
	goto OneIsland_KindleRoad_EventScript_TransSpark3

OneIsland_KindleRoad_EventScript_ShowSpark2::
	clearflag FLAG_HIDE_ECHO1_SPARK2
	goto OneIsland_KindleRoad_EventScript_TransSpark3

OneIsland_KindleRoad_EventScript_TransSpark3::
	goto_if_unset FLAG_ECHO1_SPARK_DONE3, OneIsland_KindleRoad_EventScript_ShowSpark3
	clearflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_ShowSpark3::
	clearflag FLAG_HIDE_ECHO1_SPARK3
	setflag FLAG_HIDE_ECHO_BEAST
	end
""",1)
    s+="""
@ Topaze: Echo 1, trois etincelles menent a Raikou
OneIsland_KindleRoad_EventScript_EchoSpark1::
	lock
	faceplayer
	setvar VAR_0x8004, SPECIES_VOLTORB
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark1
	setflag FLAG_ECHO1_SPARK_DONE1
	setflag FLAG_HIDE_ECHO1_SPARK1
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

OneIsland_KindleRoad_EventScript_EchoSpark2::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark2
	setflag FLAG_ECHO1_SPARK_DONE2
	setflag FLAG_HIDE_ECHO1_SPARK2
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	release
	end

OneIsland_KindleRoad_EventScript_EchoSpark3::
	lock
	faceplayer
	playmoncry SPECIES_VOLTORB, CRY_MODE_ENCOUNTER
	waitmoncry
	msgbox OneIsland_KindleRoad_Text_EchoSpark3
	setflag FLAG_ECHO1_SPARK_DONE3
	setflag FLAG_HIDE_ECHO1_SPARK3
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	clearflag FLAG_HIDE_ECHO_BEAST
	addobject LOCALID_ONE_ISLAND_RAIKOU
	playse SE_THUNDER
	delay 30
	playse SE_THUNDER2
	msgbox OneIsland_KindleRoad_Text_EchoSpark3b
	release
	end
"""
    open(sp,'w').write(s)
tp='data/maps/OneIsland_KindleRoad/text.inc'; t=open(tp).read()
if 'EchoSpark1' not in t:
    t+="""
OneIsland_KindleRoad_Text_EchoSpark1::
    .string "A crackling spark of the ECHO!\\p"
    .string "It hums, then flies off down\\n"
    .string "the road. Follow it!$"

OneIsland_KindleRoad_Text_EchoSpark2::
    .string "The spark hisses. The storm\\n"
    .string "grows louder.\\p"
    .string "Something big is down there.$"

OneIsland_KindleRoad_Text_EchoSpark3::
    .string "The last spark bursts in a\\n"
    .string "flash of blue light!$"

OneIsland_KindleRoad_Text_EchoSpark3b::
    .string "Thunder shakes the ground.\\p"
    .string "A beast of lightning waits at\\n"
    .string "the end of the road!$"
"""
    open(tp,'w').write(t)
print('ok')
