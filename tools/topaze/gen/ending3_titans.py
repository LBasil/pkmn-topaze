#!/usr/bin/env python3
"""Fin 3 : les trois Titans (Groudon, Kyogre, Rayquaza), rencontres statiques capturables apres la Reconquete (VAR_REBELS_ROUND == 9). Generateur unique (idempotent)."""
import re, json, os
T = [  # carte, label, espece, gfx, x, y, hide, fought, cri
 ('MtEmber_RubyPath_1F', 'Groudon', 'SPECIES_GROUDON', 'OBJ_EVENT_GFX_HO_OH', 22, 13, 'FLAG_HIDE_TITAN_GROUDON', 'FLAG_FOUGHT_TITAN_GROUDON'),
 ('SeafoamIslands_B4F', 'Kyogre', 'SPECIES_KYOGRE', 'OBJ_EVENT_GFX_LUGIA', 19, 9, 'FLAG_HIDE_TITAN_KYOGRE', 'FLAG_FOUGHT_TITAN_KYOGRE'),
 ('IndigoPlateau_Exterior', 'Rayquaza', 'SPECIES_RAYQUAZA', 'OBJ_EVENT_GFX_DEOXYS_N', 9, 8, 'FLAG_HIDE_TITAN_RAYQUAZA', 'FLAG_FOUGHT_TITAN_RAYQUAZA'),
]
fl = open('include/constants/flags.h').read()
for a, b in (('FLAG_0x0EC', 'FLAG_HIDE_TITAN_GROUDON'), ('FLAG_0x0ED', 'FLAG_HIDE_TITAN_KYOGRE'), ('FLAG_0x0EE', 'FLAG_HIDE_TITAN_RAYQUAZA'), ('FLAG_0x0EF', 'FLAG_FOUGHT_TITAN_GROUDON'), ('FLAG_0x0FB', 'FLAG_FOUGHT_TITAN_KYOGRE'), ('FLAG_0x0FC', 'FLAG_FOUGHT_TITAN_RAYQUAZA')):
    if b not in fl:
        fl = re.sub(r'#define %s\s+(0x[0-9A-Fa-f]+)' % a, lambda m: '#define %s %s // Topaze: fin 3, Titans' % (b, m.group(1)), fl)
open('include/constants/flags.h', 'w').write(fl)
for m, lab, sp, gfx, x, y, hide, fought in T:
    d = 'data/maps/%s/' % m; s = open(d + 'scripts.inc').read()
    if '_EventScript_Titan::' in s: continue
    setup = f'''
{m}_EventScript_TitanSetup::
	setflag {hide}
	goto_if_set {fought}, EventScript_Return
	goto_if_ne VAR_TOPAZE_ENDING, 3, EventScript_Return
	goto_if_ne VAR_REBELS_ROUND, 9, EventScript_Return
	clearflag {hide}
	return

{m}_EventScript_Titan::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	msgbox {m}_Text_TitanIntro
	setwildbattle {sp}, 0
	waitse
	playmoncry {sp}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {m}_EventScript_TitanWon
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {m}_EventScript_TitanRan
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {m}_EventScript_TitanRan
	setflag {fought}
	setflag {hide}
	release
	end

{m}_EventScript_TitanWon::
	setflag {fought}
	goto EventScript_RemoveStaticMon
	end

{m}_EventScript_TitanRan::
	setvar VAR_0x8004, {sp}
	goto EventScript_MonFlewAway
	end
'''
    mt = re.search(r'map_script MAP_SCRIPT_ON_TRANSITION, (\w+)', s)
    if mt:
        lab_tr = mt.group(1)
        s = s.replace(lab_tr + '::\n', lab_tr + '::\n\tcall %s_EventScript_TitanSetup\n' % m, 1)
    else:
        s = s.replace('\t.byte 0\n', '\tmap_script MAP_SCRIPT_ON_TRANSITION, %s_OnTransitionTitan\n\t.byte 0\n' % m, 1)
        s += f'\n{m}_OnTransitionTitan::\n\tcall {m}_EventScript_TitanSetup\n\tend\n'
    s += setup
    open(d + 'scripts.inc', 'w').write(s)
    s = open(d + 'scripts.inc').read()
    s += f'\n{m}_Text_TitanIntro::\n\t.string "A presence older than the legends\\n"\n\t.string "rises before you...\\p"\n\t.string "It has waited for a ruler worthy\\n"\n\t.string "of the throne. Show it yours!$"\n'
    open(d + 'scripts.inc', 'w').write(s)
    j = json.load(open(d + 'map.json'))
    j['object_events'].append({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3, 'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 0, 'movement_range_y': 0,
        'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': '0', 'script': f'{m}_EventScript_Titan', 'flag': hide})
    json.dump(j, open(d + 'map.json', 'w'), indent=2); open(d + 'map.json', 'a').write('\n')
print('ok')
