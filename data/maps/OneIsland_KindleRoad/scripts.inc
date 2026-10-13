OneIsland_KindleRoad_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, OneIsland_KindleRoad_OnTransition
	.byte 0

OneIsland_KindleRoad_OnTransition::
	goto_if_set FLAG_ECHO_BEAST_DONE, OneIsland_KindleRoad_EventScript_HideBeast
	goto_if_ne VAR_ECHO_STAGE, 1, OneIsland_KindleRoad_EventScript_HideBeast
	clearflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_HideBeast::
	setflag FLAG_HIDE_ECHO_BEAST
	end

OneIsland_KindleRoad_EventScript_RouteSign::
	msgbox OneIsland_KindleRoad_Text_RouteSign, MSGBOX_SIGN
	end

OneIsland_KindleRoad_EventScript_EmberSpaSign::
	msgbox OneIsland_KindleRoad_Text_EmberSpaSign, MSGBOX_SIGN
	end

@ Topaze: Echo 1 beast (static, stays if fled)
OneIsland_KindleRoad_EventScript_Raikou::
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
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, OneIsland_KindleRoad_EventScript_DefeatedRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, OneIsland_KindleRoad_EventScript_RanFromRaikou
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, OneIsland_KindleRoad_EventScript_RanFromRaikou
	setflag FLAG_ECHO_BEAST_DONE
	setflag FLAG_HIDE_ECHO_BEAST
	setvar VAR_ECHO_STAGE, 2
	release
	end

OneIsland_KindleRoad_EventScript_DefeatedRaikou::
	setflag FLAG_ECHO_BEAST_DONE
	setvar VAR_ECHO_STAGE, 2
	goto EventScript_RemoveStaticMon
	end

OneIsland_KindleRoad_EventScript_RanFromRaikou::
	setvar VAR_0x8004, SPECIES_RAIKOU
	goto EventScript_MonFlewAway
	end
