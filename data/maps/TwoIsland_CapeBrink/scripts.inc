TwoIsland_CapeBrink_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, TwoIsland_CapeBrink_OnTransition
	.byte 0

TwoIsland_CapeBrink_OnTransition::
	goto_if_set FLAG_ECHO_BEAST2_DONE, TwoIsland_CapeBrink_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 4, TwoIsland_CapeBrink_EventScript_HideBeast
	clearflag FLAG_HIDE_ECHO_BEAST2
	end

TwoIsland_CapeBrink_EventScript_HideBeast::
	setflag FLAG_HIDE_ECHO_BEAST2
	end

@ Topaze: Echo 2 beast (static, stays if fled)
TwoIsland_CapeBrink_EventScript_Entei::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_ENTEI, 0
	waitse
	playmoncry SPECIES_ENTEI, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, TwoIsland_CapeBrink_EventScript_DefeatedEntei
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, TwoIsland_CapeBrink_EventScript_RanFromEntei
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, TwoIsland_CapeBrink_EventScript_RanFromEntei
	setflag FLAG_ECHO_BEAST2_DONE
	setflag FLAG_HIDE_ECHO_BEAST2
	setvar VAR_ECHO_STAGE, 5
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone2
	end

TwoIsland_CapeBrink_EventScript_DefeatedEntei::
	setflag FLAG_ECHO_BEAST2_DONE
	setvar VAR_ECHO_STAGE, 5
	fadescreen FADE_TO_BLACK
	removeobject VAR_LAST_TALKED
	fadescreen FADE_FROM_BLACK
	goto OneIsland_PokemonCenter_1F_EventScript_EchoPhone2
	end

TwoIsland_CapeBrink_EventScript_RanFromEntei::
	setvar VAR_0x8004, SPECIES_ENTEI
	goto EventScript_MonFlewAway
	end

@ Topaze: la bouche de grotte (8,24) reste fermee tant que l'Echo n'est pas ouvert
TwoIsland_CapeBrink_EventScript_DenLocked::
	lockall
	msgbox TwoIsland_CapeBrink_Text_DenLocked
	applymovement LOCALID_PLAYER, TwoIsland_CapeBrink_Movement_DenBack
	waitmovement 0
	releaseall
	end

TwoIsland_CapeBrink_Movement_DenBack::
	walk_down
	step_end
