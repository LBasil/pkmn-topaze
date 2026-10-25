#!/usr/bin/env python3
"""Sommet de Sevault : RED reste apres la scene ; lui parler = duel 1v1 optionnel (trainer BIKER_1 reecrit). Soin apres Giovanni. Idempotent."""
import re,json
rd=lambda p:open(p).read(); wr=lambda p,s:open(p,'w').write(s)
S='SevenIsland_SevaultCanyon'; D=S+'_Summit'
sp=f'data/maps/{S}/scripts.inc'; s=rd(sp)
if f'{D}_EventScript_Red::' in rd(f'data/maps/{D}/scripts.inc'): print('deja'); raise SystemExit
trs=rd('src/data/trainers.h'); pa=rd('src/data/trainer_parties.h')
bb=re.search(r'\[TRAINER_BIKER_1\] = \{.*?\n    \},',trs,re.S).group(0)
nb=re.sub(r'trainerClass = \w+','trainerClass = TRAINER_CLASS_PKMN_TRAINER',bb)
nb=re.sub(r'trainerPic = \w+','trainerPic = TRAINER_PIC_RED',nb)
nb=re.sub(r'trainerName = _\("[^"]*"\)','trainerName = _("RED")',nb)
nb=re.sub(r'items = \{[^}]*\}','items = {ITEM_FULL_RESTORE, ITEM_FULL_RESTORE}',nb)
nb=re.sub(r'aiFlags = [\w |]+','aiFlags = AI_SCRIPT_CHECK_BAD_MOVE | AI_SCRIPT_TRY_TO_FAINT | AI_SCRIPT_CHECK_VIABILITY',nb)
nb=re.sub(r'encounterMusic_gender = [\w |]+','encounterMusic_gender = TRAINER_ENCOUNTER_MUSIC_MALE',nb)
sym=re.search(r'MOVES\((\w+)\)',nb).group(1)
trs=trs.replace(bb,nb)
m=re.search(r'static const struct TrainerMon\w+ %s\[\] = \{.*?\};'%sym,pa,re.S)
team=[('PIKACHU',77),('ESPEON',74),('SNORLAX',75),('VENUSAUR',76),('CHARIZARD',76),('BLASTOISE',77)]
body=''.join('    {\n        .iv = 60,\n        .lvl = %d,\n        .species = SPECIES_%s,\n    },\n'%(lv,sp_) for sp_,lv in team)
pa=pa.replace(m.group(0),'static const struct TrainerMonNoItemDefaultMoves %s[] = {\n%s};'%(sym,body))
wr('src/data/trainers.h',trs); wr('src/data/trainer_parties.h',pa)
# map : PNJ Red, visible apres la scene (flag TEMP_11)
mp=f'data/maps/{D}/map.json'; mj=json.load(open(mp))
mj['object_events'].append({"graphics_id":"OBJ_EVENT_GFX_RED_NORMAL","x":5,"y":4,"elevation":3,"movement_type":"MOVEMENT_TYPE_FACE_DOWN","movement_range_x":0,"movement_range_y":0,
  "trainer_type":"TRAINER_TYPE_NORMAL","trainer_sight_or_berry_tree_id":"0","script":f"{D}_EventScript_Red","flag":"FLAG_TEMP_11"})
json.dump(mj,open(mp,'w'),indent=2); open(mp,'a').write('\n')
ds=rd(f'data/maps/{D}/scripts.inc')
ds=ds.replace('\tsetflag FLAG_HIDE_ECHO_SCENE\n\tend\n','\tsetflag FLAG_HIDE_ECHO_SCENE\n\tsetflag FLAG_TEMP_11\n\tcall_if_eq VAR_ECHO_STAGE, 22, '+D+'_EventScript_ShowRed\n\tend\n\n'+D+'_EventScript_ShowRed::\n\tclearflag FLAG_TEMP_11\n\treturn\n',1)
ds+=f"""
{D}_EventScript_Red::
	trainerbattle_single TRAINER_BIKER_1, {D}_Text_RedIntro, {D}_Text_RedDefeat, {D}_EventScript_RedWon
	msgbox {D}_Text_RedPost, MSGBOX_AUTOCLOSE
	end

{D}_EventScript_RedWon::
	special HealPlayerParty
	msgbox {D}_Text_RedPost, MSGBOX_DEFAULT
	releaseall
	end
"""
wr(f'data/maps/{D}/scripts.inc',ds)
wr(f'data/maps/{D}/text.inc',rd(f'data/maps/{D}/text.inc')+f'''
{D}_Text_RedIntro::
    .string "...\\p"
    .string "(RED pulls his cap down. The air\\n"
    .string "grows heavy. He wants a duel.)$"

{D}_Text_RedDefeat::
    .string "...!$"

{D}_Text_RedPost::
    .string "...\\p"
    .string "(He tips his cap. A rare smile.)$"
''')
# soin apres Giovanni + Red2
old='\ttrainerbattle_no_intro TRAINER_ECHO_GIOVANNI, SevenIsland_SevaultCanyon_Text_SceneGiovanniDefeat\n'; assert old in s
s=s.replace(old,old+'\tspecial HealPlayerParty\n',1); wr(sp,s)
tp=f'data/maps/{S}/text.inc'; t=rd(tp)
t=re.sub(rf'{S}_Text_SceneRed2::\n(?:    \.string.*\n)+',lambda m:f'{S}_Text_SceneRed2::\n    .string "RED: ...\\p"\n    .string "(He tips his cap. Then he taps his\\n"\n    .string "chest. He is ready, whenever you\\l"\n    .string "are.)$"\n',t,1)
wr(tp,t); print('ok')
