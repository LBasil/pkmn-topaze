#!/usr/bin/env python3
"""Echo 3 (post-game) : Celio envoie au Bond Bridge (ile 3), Suicune niv. 50, Celio donne KAIMINUS (Totodile) niv. 30.
VAR_ECHO_STAGE : 6 -> 7 (Celio annonce) -> 8 (Suicune resolu) -> 9 (Totodile donne). FLAG_HIDE_ECHO_BEAST3 0x0C4, FLAG_ECHO_BEAST3_DONE 0x0C5. Non rejouable."""
import json, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_HIDE_ECHO_BEAST3' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
s = rd('include/constants/flags.h')
s = s.replace('#define FLAG_0x0C4               0x0C4', '#define FLAG_HIDE_ECHO_BEAST3    0x0C4 // Topaze: Echo 3 beast (Suicune) on Bond Bridge', 1)
s = s.replace('#define FLAG_0x0C5               0x0C5', '#define FLAG_ECHO_BEAST3_DONE    0x0C5', 1)
wr('include/constants/flags.h', s)
P = 'OneIsland_PokemonCenter_1F'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
old = f'\tgoto_if_ge VAR_ECHO_STAGE, 3, {P}_EventScript_EchoCelioDone\n'
assert old in s
s = s.replace(old, f'\tgoto_if_eq VAR_ECHO_STAGE, 8, {P}_EventScript_EchoCelioGift3\n\tgoto_if_eq VAR_ECHO_STAGE, 7, {P}_EventScript_EchoCelioWait3\n\tgoto_if_eq VAR_ECHO_STAGE, 6, {P}_EventScript_EchoCelioEcho3\n' + old, 1)
a = s.index(f'{P}_EventScript_EchoGiftParty::'); b = s.index(f'{P}_EventScript_EchoCelioDone::')
blk = (s[a:b].replace('CHIKORITA', 'TOTODILE').replace('EchoGiftParty', 'EchoGift3Party').replace('EchoGiftPC', 'EchoGift3PC')
       .replace('EchoGiftToPC', 'EchoGift3ToPC').replace('EchoGiftEnd', 'EchoGift3End').replace('EchoGotChikorita', 'EchoGotTotodile')
       .replace('setvar VAR_ECHO_STAGE, 3', 'setvar VAR_ECHO_STAGE, 9').replace('EchoCelioNext', 'EchoCelioNext3'))
s = s.rstrip('\n') + f'''

{P}_EventScript_EchoCelioEcho3::
	msgbox {P}_Text_EchoCelioEcho3
	setvar VAR_ECHO_STAGE, 7
	clearflag FLAG_HIDE_ECHO_BEAST3
	release
	end

{P}_EventScript_EchoCelioWait3::
	msgbox {P}_Text_EchoCelioWait3
	release
	end

{P}_EventScript_EchoCelioGift3::
	msgbox {P}_Text_EchoCelioGift3
	setvar VAR_TEMP_1, SPECIES_TOTODILE
	givemon SPECIES_TOTODILE, 30
	goto_if_eq VAR_RESULT, 0, {P}_EventScript_EchoGift3Party
	goto_if_eq VAR_RESULT, 1, {P}_EventScript_EchoGift3PC
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	release
	end

{blk.rstrip()}
'''
wr(f, s)
f = f'data/maps/{P}/text.inc'; s = rd(f)
wr(f, s.rstrip('\n') + f'''

{P}_Text_EchoCelioEcho3::
    .string "CELIO: BILL's compass is\\n"
    .string "ringing again!\\p"
    .string "The third ECHO is on the BOND\\n"
    .string "BRIDGE, near THREE ISLAND.\\p"
    .string "A beast of water and wind runs\\n"
    .string "there. Please be careful.$"

{P}_Text_EchoCelioWait3::
    .string "CELIO: BOND BRIDGE, THREE\\n"
    .string "ISLAND. The beast moves fast.$"

{P}_Text_EchoCelioGift3::
    .string "CELIO: The ECHO is closed!\\n"
    .string "The air feels clear again.\\p"
    .string "Another POKéMON came through.\\n"
    .string "It wants to travel with you.$"

{P}_Text_EchoGotTotodile::
    .string "{{PLAYER}} received TOTODILE!$"

{P}_Text_EchoCelioNext3::
    .string "CELIO: Three ECHOES closed.\\n"
    .string "The fourth is on FOUR ISLAND.$"
''')
P = 'ThreeIsland_BondBridge'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
head = f'{P}_MapScripts::\n\t.byte 0\n'
if head not in s: print(s[:200]); sys.exit(1)
s = s.replace(head,
 f'{P}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {P}_OnTransition\n\t.byte 0\n\n'
 f'{P}_OnTransition::\n\tgoto_if_set FLAG_ECHO_BEAST3_DONE, {P}_EventScript_HideBeast\n\tgoto_if_ne VAR_ECHO_STAGE, 7, {P}_EventScript_HideBeast\n\tclearflag FLAG_HIDE_ECHO_BEAST3\n\tend\n\n'
 f'{P}_EventScript_HideBeast::\n\tsetflag FLAG_HIDE_ECHO_BEAST3\n\tend\n', 1)
wr(f, s.rstrip('\n') + f'''

@ Topaze: Echo 3 beast (static, stays if fled)
{P}_EventScript_Suicune::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_SUICUNE, 50
	waitse
	playmoncry SPECIES_SUICUNE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_DefeatedSuicune
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFromSuicune
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFromSuicune
	setflag FLAG_ECHO_BEAST3_DONE
	setflag FLAG_HIDE_ECHO_BEAST3
	setvar VAR_ECHO_STAGE, 8
	release
	end

{P}_EventScript_DefeatedSuicune::
	setflag FLAG_ECHO_BEAST3_DONE
	setvar VAR_ECHO_STAGE, 8
	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFromSuicune::
	setvar VAR_0x8004, SPECIES_SUICUNE
	goto EventScript_MonFlewAway
	end
''')
j = json.load(open(f'data/maps/{P}/map.json'))
j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_SUICUNE', 'x': 30, 'y': 10, 'elevation': 3,
  'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
  'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_Suicune', 'flag': 'FLAG_HIDE_ECHO_BEAST3'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo3 ok')
