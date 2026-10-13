#!/usr/bin/env python3
"""Echo 7 (post-game, finale, ile 7 Sevault Canyon). Bill : stage 18 annonce -> 19 (Celebi niv. 60 apparait) -> 20 (Celebi resolu) ->
Bill epilogue -> 21 (les legendes de l'Echo apparaissent : Kyogre/Groudon/Rayquaza 70, Latias/Latios 60, Jirachi 50, statiques, reviennent s'ils fuient).
Flags 0x0CC-0x0D9 (HIDE/DONE par espece). Sprites provisoires = rocher (Celebi a son sprite). Non rejouable."""
import json, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_HIDE_ECHO_CELEBI' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
B = [  # espece, nom, niveau, x, y, stage d'apparition, sprite
 ('CELEBI', 'Celebi', 60, 13, 5, 19, 'OBJ_EVENT_GFX_CELEBI'),
 ('KYOGRE', 'Kyogre', 70, 10, 4, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
 ('GROUDON', 'Groudon', 70, 12, 4, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
 ('RAYQUAZA', 'Rayquaza', 70, 14, 4, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
 ('LATIAS', 'Latias', 60, 16, 4, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
 ('LATIOS', 'Latios', 60, 11, 5, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
 ('JIRACHI', 'Jirachi', 50, 15, 5, 21, 'OBJ_EVENT_GFX_PUSHABLE_BOULDER'),
]
s = rd('include/constants/flags.h')
n = 0xCC
for sp, *_ in B:
    for kind in ('HIDE', 'DONE'):
        old = f'#define FLAG_0x{n:03X}               0x{n:03X}'
        assert old in s, old
        s = s.replace(old, f'#define FLAG_{kind}_ECHO_{sp:<10} 0x{n:03X}', 1); n += 1
wr('include/constants/flags.h', s)
C = 'OneIsland_PokemonCenter_1F'
cf = f'data/maps/{C}/scripts.inc'; cs = rd(cf)
anchor = f'\tgoto_if_ge VAR_ECHO_STAGE, 1, {C}_EventScript_EchoBillAfter\n'
assert anchor in cs
cs = cs.replace(anchor, f'\tgoto_if_eq VAR_ECHO_STAGE, 20, {C}_EventScript_Echo7Epilogue\n\tgoto_if_eq VAR_ECHO_STAGE, 19, {C}_EventScript_Echo7Wait\n\tgoto_if_eq VAR_ECHO_STAGE, 18, {C}_EventScript_Echo7Announce\n' + anchor, 1)
wr(cf, cs.rstrip('\n') + f'''

@ Topaze: Echo 7 (finale)
{C}_EventScript_Echo7Announce::
	msgbox {C}_Text_Echo7Announce
	setvar VAR_ECHO_STAGE, 19
	release
	end

{C}_EventScript_Echo7Wait::
	msgbox {C}_Text_Echo7Wait
	release
	end

{C}_EventScript_Echo7Epilogue::
	msgbox {C}_Text_Echo7Epilogue
	setvar VAR_ECHO_STAGE, 21
	release
	end
''')
ct = rd(f'data/maps/{C}/text.inc')
wr(f'data/maps/{C}/text.inc', ct.rstrip('\n') + f'''

{C}_Text_Echo7Announce::
    .string "BILL: The compass is going wild.\\p"
    .string "The last ECHO is on SEVEN ISLAND,\\n"
    .string "in SEVAULT CANYON.\\p"
    .string "It is not a beast this time.\\n"
    .string "It is the keeper of time itself.\\p"
    .string "Go, CHAMPION. We will be here.$"

{C}_Text_Echo7Wait::
    .string "BILL: SEVAULT CANYON, SEVEN\\n"
    .string "ISLAND. The keeper of time.$"

{C}_Text_Echo7Epilogue::
    .string "BILL: The clocks are ticking\\n"
    .string "right again!\\p"
    .string "The keeper told you what the wish\\n"
    .string "really did: it cracked time open.\\p"
    .string "Now the old legends of land, sea\\n"
    .string "and sky have gathered at the top\\l"
    .string "of SEVAULT CANYON.\\p"
    .string "They wait for a TRAINER like you.$"
''')
P = 'SevenIsland_SevaultCanyon'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
hdr = f'{P}_MapScripts::\n'
assert hdr in s
s = s.replace(hdr, hdr + f'\tmap_script MAP_SCRIPT_ON_TRANSITION, {P}_OnTransition\n', 1)
t = f'\n@ Topaze: Echo 7 finale: keeper of time + gathered legends (static, stay if fled)\n{P}_OnTransition::\n'
for sp, nm, lv, x, y, st, gfx in B:
    t += f'\tsetflag FLAG_HIDE_ECHO_{sp}\n\tcall_if_unset FLAG_DONE_ECHO_{sp}, {P}_EventScript_Maybe{nm}\n'
t += '\tend\n\n'
for sp, nm, lv, x, y, st, gfx in B:
    cond = f'goto_if_ne VAR_ECHO_STAGE, {st}, EventScript_Return' if sp == 'CELEBI' else f'goto_if_ne VAR_ECHO_STAGE, {st}, EventScript_Return'
    t += f'{P}_EventScript_Maybe{nm}::\n\t{cond}\n\tclearflag FLAG_HIDE_ECHO_{sp}\n\treturn\n\n'
    after = 20 if sp == 'CELEBI' else None
    t += f'''{P}_EventScript_{nm}::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_{sp}, {lv}
	waitse
	playmoncry SPECIES_{sp}, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_Defeated{nm}
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFrom{nm}
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFrom{nm}
	setflag FLAG_DONE_ECHO_{sp}
	setflag FLAG_HIDE_ECHO_{sp}
{('	setvar VAR_ECHO_STAGE, 20' + chr(10)) if after else ''}	release
	end

{P}_EventScript_Defeated{nm}::
	setflag FLAG_DONE_ECHO_{sp}
{('	setvar VAR_ECHO_STAGE, 20' + chr(10)) if after else ''}	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFrom{nm}::
	setvar VAR_0x8004, SPECIES_{sp}
	goto EventScript_MonFlewAway
	end

'''
wr(f, s.rstrip('\n') + '\n' + t.rstrip('\n') + '\n')
j = json.load(open(f'data/maps/{P}/map.json'))
for sp, nm, lv, x, y, st, gfx in B:
    j['object_events'].append({'graphics_id': gfx, 'x': x, 'y': y, 'elevation': 3,
      'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
      'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_{nm}', 'flag': f'FLAG_HIDE_ECHO_{sp}'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo7 ok')
