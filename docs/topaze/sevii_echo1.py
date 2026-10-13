#!/usr/bin/env python3
"""Echo 1 (post-game) : Bill + Celio au Centre de l'ile 1 (compas, indice), Raikou sur la Kindle Road, cadeau CHIKORITA par Celio.
VAR_ECHO_STAGE (0x402D) : 0 rien, 1 compas donne, 2 Raikou resolu, 3 Chikorita donne. FLAG_HIDE_ECHO_BEAST (0x0C0). Non rejouable."""
import json, re, sys
rd = lambda p: open(p).read(); wr = lambda p, s: open(p, 'w').write(s)
if 'VAR_ECHO_STAGE' in rd('include/constants/vars.h'): print('already'); sys.exit(0)
RAIKOU_POS = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (12, 120)
s = rd('include/constants/vars.h')
wr('include/constants/vars.h', s.replace('#define VAR_TOURNAMENT_ROUND', '#define VAR_ECHO_STAGE VAR_0x402D // post-game Echoes: 0 none, 1 compass, 2 beast done, 3 gift given\n#define VAR_TOURNAMENT_ROUND', 1))
s = rd('include/constants/flags.h')
wr('include/constants/flags.h', s.replace('#define FLAG_0x0C0               0x0C0', '#define FLAG_HIDE_ECHO_BEAST     0x0C0 // Topaze: Echo 1 beast (Raikou) on Kindle Road', 1).replace('#define FLAG_0x0C1               0x0C1', '#define FLAG_ECHO_BEAST_DONE     0x0C1', 1))

# ---------- Pokemon Center 1F
P = 'OneIsland_PokemonCenter_1F'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
# transition : Bill et Celio visibles en post-game, sans la scene vanilla
s = s.replace(f'{P}_OnTransition::\n\tsetrespawn HEAL_LOCATION_ONE_ISLAND\n',
 f'{P}_OnTransition::\n\tsetrespawn HEAL_LOCATION_ONE_ISLAND\n\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_PostgameSetup\n', 1)
s = s.replace(f'{P}_EventScript_SetCelioQuestDone::',
 f'''@ Topaze: post-game, Bill and Celio wait here (Echoes). Skip the vanilla first-meeting scene.
{P}_EventScript_PostgameSetup::
	clearflag FLAG_HIDE_ONE_ISLAND_POKECENTER_BILL
	clearflag FLAG_HIDE_ONE_ISLAND_POKECENTER_CELIO
	setvar VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F, 7
	setobjectxyperm LOCALID_ONE_ISLAND_POKEMON_CENTER_BILL, 14, 6
	setobjectmovementtype LOCALID_ONE_ISLAND_POKEMON_CENTER_BILL, MOVEMENT_TYPE_FACE_DOWN
	setobjectxyperm LOCALID_CELIO, 15, 6
	setobjectmovementtype LOCALID_CELIO, MOVEMENT_TYPE_FACE_DOWN
	end

{P}_EventScript_SetCelioQuestDone::''', 1)
s = s.replace(f'{P}_EventScript_Bill::\n\tlock\n',
 f'{P}_EventScript_Bill::\n\tlock\n\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_EchoBill\n', 1)
s = s.replace(f'{P}_EventScript_Celio::\n\tlock\n\tfaceplayer\n',
 f'{P}_EventScript_Celio::\n\tlock\n\tfaceplayer\n\tgoto_if_set FLAG_TOPAZE_POSTGAME, {P}_EventScript_EchoCelio\n', 1)
s = s.rstrip('\n') + f'''

@ Topaze: Echoes of Time, island 1
{P}_EventScript_EchoBill::
	applymovement LOCALID_ONE_ISLAND_POKEMON_CENTER_BILL, Common_Movement_FacePlayer
	waitmovement 0
	goto_if_ge VAR_ECHO_STAGE, 1, {P}_EventScript_EchoBillAfter
	msgbox {P}_Text_EchoBillIntro
	giveitem_msg {P}_Text_EchoReceivedCompass, ITEM_VS_SEEKER, 1, MUS_OBTAIN_KEY_ITEM
	msgbox {P}_Text_EchoBillCompass
	setvar VAR_ECHO_STAGE, 1
	clearflag FLAG_HIDE_ECHO_BEAST
	release
	end

{P}_EventScript_EchoBillAfter::
	msgbox {P}_Text_EchoBillAfter
	release
	end

{P}_EventScript_EchoCelio::
	goto_if_ge VAR_ECHO_STAGE, 3, {P}_EventScript_EchoCelioDone
	goto_if_eq VAR_ECHO_STAGE, 2, {P}_EventScript_EchoCelioGift
	goto_if_eq VAR_ECHO_STAGE, 1, {P}_EventScript_EchoCelioWait
	msgbox {P}_Text_EchoCelioHello
	release
	end

{P}_EventScript_EchoCelioWait::
	msgbox {P}_Text_EchoCelioWait
	release
	end

{P}_EventScript_EchoCelioGift::
	msgbox {P}_Text_EchoCelioGift
	setvar VAR_TEMP_1, SPECIES_CHIKORITA
	givemon SPECIES_CHIKORITA, 30
	goto_if_eq VAR_RESULT, 0, {P}_EventScript_EchoGiftParty
	goto_if_eq VAR_RESULT, 1, {P}_EventScript_EchoGiftPC
	goto_if_eq VAR_RESULT, 2, EventScript_NoMoreRoomForPokemon
	release
	end

{P}_EventScript_EchoGiftParty::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	playfanfare MUS_LEVEL_UP
	message {P}_Text_EchoGotChikorita
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_CHIKORITA
	msgbox Text_GiveNicknameToThisMon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, {P}_EventScript_EchoGiftEnd
	call EventScript_GetGiftMonPartySlot
	call EventScript_ChangePokemonNickname
	goto {P}_EventScript_EchoGiftEnd
	end

{P}_EventScript_EchoGiftPC::
	textcolor NPC_TEXT_COLOR_NEUTRAL
	playfanfare MUS_LEVEL_UP
	message {P}_Text_EchoGotChikorita
	waitmessage
	waitfanfare
	bufferspeciesname STR_VAR_1, SPECIES_CHIKORITA
	msgbox Text_GiveNicknameToThisMon, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, {P}_EventScript_EchoGiftToPC
	call EventScript_NameReceivedBoxMon
	goto {P}_EventScript_EchoGiftToPC
	end

{P}_EventScript_EchoGiftToPC::
	call EventScript_TransferredToPC
	goto {P}_EventScript_EchoGiftEnd
	end

{P}_EventScript_EchoGiftEnd::
	textcolor NPC_TEXT_COLOR_MALE
	setvar VAR_ECHO_STAGE, 3
	msgbox {P}_Text_EchoCelioNext
	release
	end

{P}_EventScript_EchoCelioDone::
	msgbox {P}_Text_EchoCelioNext
	release
	end
'''
wr(f, s)
f = f'data/maps/{P}/text.inc'; s = rd(f)
wr(f, s.rstrip('\n') + f'''

{P}_Text_EchoBillIntro::
    .string "BILL: Hey, CHAMPION! I knew\\n"
    .string "you would find me.\\p"
    .string "Since the LEAGUE, time has been\\n"
    .string "acting up all over KANTO.\\p"
    .string "Clocks run backward. Old POKéMON\\n"
    .string "show up where they should not.\\p"
    .string "I call them ECHOES: pieces of\\n"
    .string "other lands and other times.\\p"
    .string "They wash up on these islands.\\p"
    .string "CELIO and I built a device to\\n"
    .string "find them. Take it.$"

{P}_Text_EchoReceivedCompass::
    .string "{{PLAYER}} received the TIME COMPASS!$"

{P}_Text_EchoBillCompass::
    .string "BILL: It points at the nearest\\n"
    .string "ECHO.\\p"
    .string "The first one is on KINDLE ROAD.\\n"
    .string "A beast of lightning runs there.\\p"
    .string "Calm it down, then see CELIO.$"

{P}_Text_EchoBillAfter::
    .string "BILL: Every ECHO you close makes\\n"
    .string "the world a little steadier.$"

{P}_Text_EchoCelioHello::
    .string "CELIO: Welcome back, CHAMPION.\\p"
    .string "BILL will explain everything.$"

{P}_Text_EchoCelioWait::
    .string "CELIO: The first ECHO is on\\n"
    .string "KINDLE ROAD. Be careful.$"

{P}_Text_EchoCelioGift::
    .string "CELIO: You closed the ECHO!\\p"
    .string "A POKéMON came through it.\\n"
    .string "It chose to follow you.$"

{P}_Text_EchoGotChikorita::
    .string "{{PLAYER}} received CHIKORITA!$"

{P}_Text_EchoCelioNext::
    .string "CELIO: The next ECHO is further\\n"
    .string "along the islands. Soon.$"
''')

# ---------- Kindle Road : Raikou
P = 'OneIsland_KindleRoad'
f = f'data/maps/{P}/scripts.inc'; s = rd(f)
s = s.replace(f'{P}_MapScripts::\n\t.byte 0\n',
 f'{P}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, {P}_OnTransition\n\t.byte 0\n\n'
 f'{P}_OnTransition::\n\tgoto_if_set FLAG_ECHO_BEAST_DONE, {P}_EventScript_HideBeast\n\tgoto_if_ne VAR_ECHO_STAGE, 1, {P}_EventScript_HideBeast\n\tclearflag FLAG_HIDE_ECHO_BEAST\n\tend\n\n'
 f'{P}_EventScript_HideBeast::\n\tsetflag FLAG_HIDE_ECHO_BEAST\n\tend\n', 1)
wr(f, s.rstrip('\n') + f'''

@ Topaze: Echo 1 beast (static, stays if fled)
{P}_EventScript_Raikou::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_RAIKOU, 45
	waitse
	playmoncry SPECIES_RAIKOU, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, {P}_EventScript_DefeatedRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, {P}_EventScript_RanFromRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, {P}_EventScript_RanFromRaikou
	setflag FLAG_ECHO_BEAST_DONE
	setflag FLAG_HIDE_ECHO_BEAST
	setvar VAR_ECHO_STAGE, 2
	release
	end

{P}_EventScript_DefeatedRaikou::
	setflag FLAG_ECHO_BEAST_DONE
	setvar VAR_ECHO_STAGE, 2
	goto EventScript_RemoveStaticMon
	end

{P}_EventScript_RanFromRaikou::
	setvar VAR_0x8004, SPECIES_RAIKOU
	goto EventScript_MonFlewAway
	end
''')
j = json.load(open(f'data/maps/{P}/map.json'))
j['object_events'].append({'graphics_id': 'OBJ_EVENT_GFX_RAIKOU', 'x': RAIKOU_POS[0], 'y': RAIKOU_POS[1], 'elevation': 3,
  'movement_type': 'MOVEMENT_TYPE_FACE_DOWN', 'movement_range_x': 1, 'movement_range_y': 1, 'trainer_type': 'TRAINER_TYPE_NONE',
  'trainer_sight_or_berry_tree_id': '0', 'script': f'{P}_EventScript_Raikou', 'flag': 'FLAG_HIDE_ECHO_BEAST'})
json.dump(j, open(f'data/maps/{P}/map.json', 'w'), indent=2); open(f'data/maps/{P}/map.json', 'a').write('\n')
print('echo1 ok')
