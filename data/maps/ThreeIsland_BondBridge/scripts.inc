ThreeIsland_BondBridge_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, ThreeIsland_BondBridge_OnTransition
	.byte 0

ThreeIsland_BondBridge_OnTransition::
	goto_if_set FLAG_ECHO_BEAST3_DONE, ThreeIsland_BondBridge_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 7, ThreeIsland_BondBridge_EventScript_HideBeast
	clearflag FLAG_HIDE_ECHO_BEAST3
	end

ThreeIsland_BondBridge_EventScript_HideBeast::
	setflag FLAG_HIDE_ECHO_BEAST3
	end

ThreeIsland_BondBridge_EventScript_BerryForestSign::
	msgbox ThreeIsland_BondBridge_Text_BerryForestAhead, MSGBOX_SIGN
	end

ThreeIsland_BondBridge_EventScript_BondBridgeSign::
	msgbox ThreeIsland_BondBridge_Text_BondBridgeSign, MSGBOX_SIGN
	end

@ Topaze: Echo 3 beast (static, stays if fled)
ThreeIsland_BondBridge_EventScript_Suicune::
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
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, ThreeIsland_BondBridge_EventScript_DefeatedSuicune
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, ThreeIsland_BondBridge_EventScript_RanFromSuicune
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, ThreeIsland_BondBridge_EventScript_RanFromSuicune
	setflag FLAG_ECHO_BEAST3_DONE
	setflag FLAG_HIDE_ECHO_BEAST3
	setvar VAR_ECHO_STAGE, 8
	release
	end

ThreeIsland_BondBridge_EventScript_DefeatedSuicune::
	setflag FLAG_ECHO_BEAST3_DONE
	setvar VAR_ECHO_STAGE, 8
	goto EventScript_RemoveStaticMon
	end

ThreeIsland_BondBridge_EventScript_RanFromSuicune::
	setvar VAR_0x8004, SPECIES_SUICUNE
	goto EventScript_MonFlewAway
	end
