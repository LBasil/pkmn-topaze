#!/usr/bin/env python3
"""Echo 2 (post-game) : Bill envoie au Cap Brink (ile 2), Entei niv. 48 (statique, revient s'il fuit), Bill donne HERISSON (Cyndaquil) niv. 30.
VAR_ECHO_STAGE : 3 -> 4 (Bill annonce) -> 5 (Entei resolu) -> 6 (Cyndaquil donne). FLAG_HIDE_ECHO_BEAST2 0x0C2, FLAG_ECHO_BEAST2_DONE 0x0C3. Non rejouable."""
import json, re, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_HIDE_ECHO_BEAST2' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
s = rd('include/constants/flags.h')
s = s.replace('#define FLAG_0x0C2               0x0C2', '#define FLAG_HIDE_ECHO_BEAST2    0x0C2 // Topaze: Echo 2 beast (Entei) on Cape Brink', 1)
s = s.replace('#define FLAG_0x0C3               0x0C3', '#define FLAG_ECHO_BEAST2_DONE    0x0C3', 1)
wr('include/constants/flags.h', s)
P = 'OneIsland_PokemonCenter_1F'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
# Bill : routage par etape
old = f'\tgoto_if_ge VAR_ECHO_STAGE, 1, {P}_EventScript_EchoBillAfter\n'
assert old in s
s = s.replace(old, f'\tgoto_if_eq VAR_ECHO_STAGE, 5, {P}_EventScript_EchoBillGift2\n\tgoto_if_eq VAR_ECHO_STAGE, 4, {P}_EventScript_EchoBillWait2\n\tgoto_if_eq VAR_ECHO_STAGE, 3, {P}_EventScript_EchoBillEcho2\n' + old, 1)
# bloc cadeau Chikorita -> Cyndaquil (copie)
a = s.index(f'{P}_EventScript_EchoGiftParty::'); b = s.index(f'{P}_EventScript_EchoCelioDone::')
blk = s[a:b]
blk = (blk.replace('CHIKORITA', 'CYNDAQUIL').replace('EchoGiftParty', 'EchoGift2Party').replace('EchoGiftPC', 'EchoGift2PC')
       .replace('EchoGiftToPC', 'EchoGift2ToPC').replace('EchoGiftEnd', 'EchoGift2End').replace('EchoGotChikorita', 'EchoGotCyndaquil')
       .replace('setvar VAR_ECHO_STAGE, 3', 'setvar VAR_ECHO_STAGE, 6').replace('EchoCelioNext', 'EchoBillNext2'))
s = s.rstrip('\n') + f'''

{P}_EventScript_EchoBillEcho2::
	msgbox {P}_Text_EchoBillEcho2
	setvar VAR_ECHO_STAGE, 4
	clearflag FLAG_HIDE_ECHO_BEAST2
	release
	end

{P}_EventScript_EchoBillWait2::
	msgbox {P}_Text_EchoBillWait2
	release
	end

{P}_EventScript_EchoBillGift2::
	msgbox {P}_Text_EchoBillGift2
	setvar VAR_TEMP_1, SPECIES_CYNDAQUIL
	givemon SPECIES_CYNDAQUIL, 30
	goto_if_eq VAR_RESULT, 0, {P}_EventScript_EchoGift2Party
	goto_if_eq VAR_RESULT, 1, {P}_EventScript_EchoGift2PC
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	release
	end

{blk.rstrip()}
'''
wr(f, s)
f = f'data/maps/{P}/text.inc'; s = rd(f)
wr(f, s.rstrip('\n') + f'''

{P}_Text_EchoBillEcho2::
    .string "BILL: CELIO's guess was right:\\n"
    .string "the ECHOES are linked.\\p"
    .string "The second one is on CAPE BRINK,\\n"
    .string "on TWO ISLAND.\\p"
    .string "A beast of flames guards it.\\n"
    .string "Calm it down, then come back.$"

{P}_Text_EchoBillWait2::
    .string "BILL: CAPE BRINK, on TWO ISLAND.\\n"
    .string "Watch out for the heat.$"

{P}_Text_EchoBillGift2::
    .string "BILL: The ECHO is closed! The\\n"
    .string "compass went quiet.\\p"
    .string "This POKéMON came through it.\\n"
    .string "Take care of it, CHAMPION.$"

{P}_Text_EchoGotCyndaquil::
    .string "{{PLAYER}} received CYNDAQUIL!$"

{P}_Text_EchoBillNext2::
    .string "BILL: Two ECHOES closed. The\\n"
    .string "third one is near THREE ISLAND.$"
''')
P = 'TwoIsland_CapeBrink'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
s = s.replace(f'{P}_MapScripts::\n\t.byte 0\n',
 f'{P}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {P}_OnTransition\n\t.byte 0\n\n'
 f'{P}_OnTransition::\n\tgoto_if_set FLAG_ECHO_BEAST2_DONE, {P}_EventScript_HideBeast\n\tgoto_if_ne VAR_ECHO_STAGE, 4, {P}_EventScript_HideBeast\n\tclearflag FLAG_HIDE_ECHO_BEAST2\n\tend\n\n'
 f'{P}_EventScript_HideBeast::\n\tsetflag FLAG_HIDE_ECHO_BEAST2\n\tend\n', 1)
wr(f, s.rstrip('\n') + f'''

@ Topaze: Echo 2 beast (static, stays if fled)
{P}_EventScript_Entei::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_ENTEI, 48
	waitse
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_DefeatedEntei
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFromEntei
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFromEntei
	setflag FLAG_ECHO_BEAST2_DONE
	setflag FLAG_HIDE_ECHO_BEAST2
	setvar VAR_ECHO_STAGE, 5
	release
	end

{P}_EventScript_DefeatedEntei::
	setflag FLAG_ECHO_BEAST2_DONE
	setvar VAR_ECHO_STAGE, 5
	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFromEntei::
	setvar VAR_0x8004, SPECIES_ENTEI
	goto EventScript_MonFlewAway
	end
''')
j = json.load(open(f'data/maps/{P}/map.json'))
j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_ENTEI', 'x': 12, 'y': 29, 'elevation': 3,
  'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
  'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_Entei', 'flag': 'FLAG_HIDE_ECHO_BEAST2'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo2 ok')
