#!/usr/bin/env python3
"""Echo 4 (post-game) : Lorelei (sa maison, ile 4) envoie a Icefall Cave Back, Regice niv. 52, Lorelei donne GRAINIPIOT (Treecko) niv. 30.
VAR_ECHO_STAGE : 9 -> 10 (Lorelei annonce) -> 11 (Regice resolu) -> 12 (Treecko donne). FLAG_HIDE_ECHO_BEAST4 0x0C6, FLAG_ECHO_BEAST4_DONE 0x0C7. Non rejouable."""
import json, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'FLAG_HIDE_ECHO_BEAST4' in rd('include/constants/flags.h'): print('already'); sys.exit(0)
s = rd('include/constants/flags.h')
s = s.replace('#define FLAG_0x0C6               0x0C6', '#define FLAG_HIDE_ECHO_BEAST4    0x0C6 // Topaze: Echo 4 (Regice) in Icefall Cave Back', 1)
s = s.replace('#define FLAG_0x0C7               0x0C7', '#define FLAG_ECHO_BEAST4_DONE    0x0C7', 1)
wr('include/constants/flags.h', s)
C = 'OneIsland_PokemonCenter_1F'
cs = rd(f'data/maps/{C}/scripts.inc')
a = cs.index(f'{C}_EventScript_EchoGiftParty::'); b = cs.index(f'{C}_EventScript_EchoCelioDone::')
P = 'FourIsland_LoreleisHouse'
blk = (cs[a:b].replace(C, P).replace('CHIKORITA', 'TREECKO').replace('EchoGiftParty', 'EchoGift4Party').replace('EchoGiftPC', 'EchoGift4PC')
       .replace('EchoGiftToPC', 'EchoGift4ToPC').replace('EchoGiftEnd', 'EchoGift4End').replace('EchoGotChikorita', 'EchoGotTreecko')
       .replace('setvar VAR_ECHO_STAGE, 3', 'setvar VAR_ECHO_STAGE, 12').replace('EchoCelioNext', 'EchoLoreleiNext4'))
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
old = f'{P}_EventScript_Lorelei::\n\tlock\n\tfaceplayer\n'
assert old in s
s = s.replace(old, old + f'\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_EchoLorelei\n', 1)
s = s.replace(f'{P}_OnTransition::\n', f'{P}_OnTransition::\n\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_PostgameLorelei\n', 1)
s = s.replace(f'{P}_EventScript_Lorelei::', f'''{P}_EventScript_PostgameLorelei::
	clearflag FLAG_HIDE_LORELEI_IN_HER_HOUSE
	special UpdateLoreleiDollCollection
	end

{P}_EventScript_Lorelei::''', 1)
wr(f, s.rstrip('\n') + f'''

@ Topaze: Echoes of Time, island 4
{P}_EventScript_EchoLorelei::
	goto_if_ge VAR_ECHO_STAGE, 12, {P}_EventScript_EchoLoreleiAfter
	goto_if_eq VAR_ECHO_STAGE, 11, {P}_EventScript_EchoLoreleiGift
	goto_if_eq VAR_ECHO_STAGE, 10, {P}_EventScript_EchoLoreleiWait
	goto_if_eq VAR_ECHO_STAGE, 9, {P}_EventScript_EchoLoreleiEcho
	msgbox {P}_Text_EchoLoreleiHello
	release
	end

{P}_EventScript_EchoLoreleiEcho::
	msgbox {P}_Text_EchoLoreleiEcho
	setvar VAR_ECHO_STAGE, 10
	clearflag FLAG_HIDE_ECHO_BEAST4
	release
	end

{P}_EventScript_EchoLoreleiWait::
	msgbox {P}_Text_EchoLoreleiWait
	release
	end

{P}_EventScript_EchoLoreleiAfter::
	msgbox {P}_Text_EchoLoreleiNext4
	release
	end

{P}_EventScript_EchoLoreleiGift::
	msgbox {P}_Text_EchoLoreleiGift
	setvar VAR_TEMP_1, SPECIES_TREECKO
	givemon SPECIES_TREECKO, 30
	goto_if_eq VAR_RESULT, 0, {P}_EventScript_EchoGift4Party
	goto_if_eq VAR_RESULT, 1, {P}_EventScript_EchoGift4PC
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	release
	end

{blk.rstrip()}
''')
f = f'data/maps/{P}/text.inc'; s = rd(f)
wr(f, s.rstrip('\n') + f'''

{P}_Text_EchoLoreleiHello::
    .string "LORELEI: The ice has been\\n"
    .string "strange lately, CHAMPION.$"

{P}_Text_EchoLoreleiEcho::
    .string "LORELEI: Two beasts of the old\\n"
    .string "legends passed through here.\\p"
    .string "Now the fourth ECHO is sealed in\\n"
    .string "the deepest ICEFALL CAVE.\\p"
    .string "A statue of ice walks there.\\n"
    .string "Please, calm it down.$"

{P}_Text_EchoLoreleiWait::
    .string "LORELEI: The ECHO is in the back\\n"
    .string "of ICEFALL CAVE. Stay warm.$"

{P}_Text_EchoLoreleiGift::
    .string "LORELEI: The cold has lifted.\\n"
    .string "Thank you.\\p"
    .string "A little POKéMON came with the\\n"
    .string "ECHO. It is yours now.$"

{P}_Text_EchoGotTreecko::
    .string "{{PLAYER}} received TREECKO!$"

{P}_Text_EchoLoreleiNext4::
    .string "LORELEI: Four ECHOES closed.\\n"
    .string "Ask BILL about the next one.$"
''')
P = 'FourIsland_IcefallCave_Back'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
s = s.replace(f'{P}_OnTransition::\n', f'{P}_OnTransition::\n\tcall {P}_EventScript_EchoSetup\n', 1)
wr(f, s.rstrip('\n') + f'''

@ Topaze: Echo 4 (static, stays if fled)
{P}_EventScript_EchoSetup::
	setflag FLAG_HIDE_ECHO_BEAST4
	goto_if_set FLAG_ECHO_BEAST4_DONE, EventScript_Return
	goto_if_ne VAR_ECHO_STAGE, 10, EventScript_Return
	clearflag FLAG_HIDE_ECHO_BEAST4
	return

{P}_EventScript_Regice::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_REGICE, 52
	waitse
	playmoncry SPECIES_REGICE, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_DefeatedRegice
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFromRegice
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFromRegice
	setflag FLAG_ECHO_BEAST4_DONE
	setflag FLAG_HIDE_ECHO_BEAST4
	setvar VAR_ECHO_STAGE, 11
	release
	end

{P}_EventScript_DefeatedRegice::
	setflag FLAG_ECHO_BEAST4_DONE
	setvar VAR_ECHO_STAGE, 11
	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFromRegice::
	setvar VAR_0x8004, SPECIES_REGICE
	goto EventScript_MonFlewAway
	end
''')
j = json.load(open(f'data/maps/{P}/map.json'))
j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_PUSHABLE_BOULDER', 'x': 12, 'y': 15, 'elevation': 3,
  'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
  'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_Regice', 'flag': 'FLAG_HIDE_ECHO_BEAST4'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo4 ok')
# note : EchoClearRockets (Rockets/Lorelei caches en post-game, scene=2) ajoute a la main dans Icefall Cave Back
