MtEmber_Summit_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, MtEmber_Summit_OnTransition
	map_script MAP_SCRIPT_ON_RESUME, MtEmber_Summit_OnResume
	.byte 0

MtEmber_Summit_OnResume::
	call_if_set FLAG_SYS_SPECIAL_WILD_BATTLE, MtEmber_Summit_EventScript_TryRemoveMoltres
	end

MtEmber_Summit_EventScript_TryRemoveMoltres::
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_ne VAR_RESULT, B_OUTCOME_CAUGHT, EventScript_Return
	removeobject VAR_LAST_TALKED
	return

MtEmber_Summit_OnTransition::
	setflag FLAG_0x148
	setflag FLAG_0x149
	setflag FLAG_0x14A
	setflag FLAG_0x14B
	goto_if_set FLAG_FOUGHT_MOLTRES, MtEmber_Summit_Guards_Done
	goto_if_unset FLAG_TOPAZE_POSTGAME, MtEmber_Summit_Guards_Done
	goto_if_defeated TRAINER_CHANNELER_5, MtEmber_Summit_Guards_Skip0
	clearflag FLAG_0x148
MtEmber_Summit_Guards_Skip0:
	goto_if_defeated TRAINER_CHANNELER_6, MtEmber_Summit_Guards_Skip1
	clearflag FLAG_0x149
MtEmber_Summit_Guards_Skip1:
	goto_if_defeated TRAINER_CHANNELER_7, MtEmber_Summit_Guards_Skip2
	clearflag FLAG_0x14A
MtEmber_Summit_Guards_Skip2:
	goto_if_defeated TRAINER_CHANNELER_8, MtEmber_Summit_Guards_Skip3
	clearflag FLAG_0x14B
MtEmber_Summit_Guards_Skip3:
MtEmber_Summit_Guards_Done:
	call_if_unset FLAG_FOUGHT_MOLTRES, MtEmber_Summit_EventScript_ShowMoltres
	end

MtEmber_Summit_EventScript_ShowMoltres::
	goto_if_unset FLAG_TOPAZE_POSTGAME, EventScript_Return
	clearflag FLAG_HIDE_MOLTRES
	return

MtEmber_Summit_EventScript_Moltres::
	goto_if_questlog EventScript_ReleaseEnd
	special QuestLog_CutRecording
	lock
	faceplayer
	setwildbattle SPECIES_MOLTRES, 0
	waitse
	playmoncry SPECIES_MOLTRES, CRY_MODE_ENCOUNTER
	message Text_Gyaoo
	waitmessage
	waitmoncry
	delay 10
	playbgm MUS_ENCOUNTER_GYM_LEADER, 0
	waitbuttonpress
	setflag FLAG_SYS_SPECIAL_WILD_BATTLE
	special StartLegendaryBattle
	waitstate
	clearflag FLAG_SYS_SPECIAL_WILD_BATTLE
	specialvar VAR_RESULT, GetBattleOutcome
	goto_if_eq VAR_RESULT, B_OUTCOME_WON, MtEmber_Summit_EventScript_DefeatedMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_RAN, MtEmber_Summit_EventScript_RanFromMoltres
	goto_if_eq VAR_RESULT, B_OUTCOME_PLAYER_TELEPORTED, MtEmber_Summit_EventScript_RanFromMoltres
	setflag FLAG_FOUGHT_MOLTRES
	release
	end

MtEmber_Summit_EventScript_DefeatedMoltres::
	setflag FLAG_FOUGHT_MOLTRES
	goto EventScript_RemoveStaticMon
	end

MtEmber_Summit_EventScript_RanFromMoltres::
	setvar VAR_0x8004, SPECIES_MOLTRES
	goto EventScript_MonFlewAway
	end

MtEmber_Summit_Guard0::
	trainerbattle_single TRAINER_CHANNELER_5, MtEmber_Summit_Text_Guard0Intro, MtEmber_Summit_Text_Guard0Defeat, MtEmber_Summit_Guard0_Vanish
	msgbox MtEmber_Summit_Text_Guard0Post, MSGBOX_AUTOCLOSE
	end

MtEmber_Summit_Guard0_Vanish::
	msgbox MtEmber_Summit_Text_Guard0Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x148
	removeobject VAR_LAST_TALKED
	releaseall
	end

MtEmber_Summit_Guard1::
	trainerbattle_single TRAINER_CHANNELER_6, MtEmber_Summit_Text_Guard1Intro, MtEmber_Summit_Text_Guard1Defeat, MtEmber_Summit_Guard1_Vanish
	msgbox MtEmber_Summit_Text_Guard1Post, MSGBOX_AUTOCLOSE
	end

MtEmber_Summit_Guard1_Vanish::
	msgbox MtEmber_Summit_Text_Guard1Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x149
	removeobject VAR_LAST_TALKED
	releaseall
	end

MtEmber_Summit_Guard2::
	trainerbattle_single TRAINER_CHANNELER_7, MtEmber_Summit_Text_Guard2Intro, MtEmber_Summit_Text_Guard2Defeat, MtEmber_Summit_Guard2_Vanish
	msgbox MtEmber_Summit_Text_Guard2Post, MSGBOX_AUTOCLOSE
	end

MtEmber_Summit_Guard2_Vanish::
	msgbox MtEmber_Summit_Text_Guard2Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14A
	removeobject VAR_LAST_TALKED
	releaseall
	end

MtEmber_Summit_Guard3::
	trainerbattle_single TRAINER_CHANNELER_8, MtEmber_Summit_Text_Guard3Intro, MtEmber_Summit_Text_Guard3Defeat, MtEmber_Summit_Guard3_Vanish
	msgbox MtEmber_Summit_Text_Guard3Post, MSGBOX_AUTOCLOSE
	end

MtEmber_Summit_Guard3_Vanish::
	msgbox MtEmber_Summit_Text_Guard3Post, MSGBOX_DEFAULT
	closemessage
	setflag FLAG_0x14B
	removeobject VAR_LAST_TALKED
	releaseall
	end
