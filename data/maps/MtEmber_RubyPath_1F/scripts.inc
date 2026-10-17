MtEmber_RubyPath_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtEmber_RubyPath_1F_OnTransitionTitan
	.byte 0

MtEmber_RubyPath_1F_OnTransitionTitan::
	call MtEmber_RubyPath_1F_EventScript_TitanSetup
	end

MtEmber_RubyPath_1F_EventScript_TitanSetup::
	setflag FLAG_HIDE_TITAN_GROUDON
	goto_if_set FLAG_FOUGHT_TITAN_GROUDON, EventScript_Return
	goto_if_ne VAR_TOPAZE_ENDING, 3, EventScript_Return
	goto_if_ne VAR_REBELS_ROUND, 9, EventScript_Return
	clearflag FLAG_HIDE_TITAN_GROUDON
	return

MtEmber_RubyPath_1F_EventScript_Titan::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	msgbox MtEmber_RubyPath_1F_Text_TitanIntro
	setwildbattle SPECIES_GROUDON, 0
	waitse
	playmoncry SPECIES_GROUDON, CRY_MODE_ENCOUNTER
	delay 40
	waitmoncry
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MtEmber_RubyPath_1F_EventScript_TitanWon
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtEmber_RubyPath_1F_EventScript_TitanRan
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtEmber_RubyPath_1F_EventScript_TitanRan
	setflag FLAG_FOUGHT_TITAN_GROUDON
	setflag FLAG_HIDE_TITAN_GROUDON
	release
	end

MtEmber_RubyPath_1F_EventScript_TitanWon::
	setflag FLAG_FOUGHT_TITAN_GROUDON
	goto EventScript_RemoveStaticMon
	end

MtEmber_RubyPath_1F_EventScript_TitanRan::
	setvar VAR_0x8004, SPECIES_GROUDON
	goto EventScript_MonFlewAway
	end

MtEmber_RubyPath_1F_Text_TitanIntro::
	.string "A presence older than the legends\n"
	.string "rises before you...\p"
	.string "It has waited for a ruler worthy\n"
	.string "of the throne. Show it yours!$"
