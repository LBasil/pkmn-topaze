SilphCo_9F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SilphCo_9F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SilphCo_9F_OnTransition
	.byte 0

SilphCo_9F_OnLoad::
	end

SilphCo_9F_EventScript_HealWoman::
	lock
	faceplayer
	goto_if_ge VAR_MAP_SCENE_SILPH_CO_11F, 1, SilphCo_9F_EventScript_HealWomanRocketsGone
	msgbox SilphCo_9F_Text_YouShouldTakeQuickNap
	closemessage
	call EventScript_OutOfCenterPartyHeal
	msgbox SilphCo_9F_Text_DontGiveUp
	release
	end

SilphCo_9F_EventScript_HealWomanRocketsGone::
	msgbox SilphCo_9F_Text_ThankYouSoMuch
	release
	end

SilphCo_9F_EventScript_FloorSign::
	msgbox SilphCo_9F_Text_FloorSign, MSGBOX_SIGN
	end

SilphCo_9F_EventScript_Ed::
	trainerbattle_single TRAINER_SCIENTIST_ED, SilphCo_9F_Text_EdIntro, SilphCo_9F_Text_EdDefeat
	msgbox SilphCo_9F_Text_EdPostBattle, MSGBOX_AUTOCLOSE
	end

SilphCo_9F_EventScript_Grunt1::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_37, SilphCo_9F_Text_Grunt1Intro, SilphCo_9F_Text_Grunt1Defeat
	msgbox SilphCo_9F_Text_Grunt1PostBattle, MSGBOX_AUTOCLOSE
	end

SilphCo_9F_EventScript_Grunt2::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_38, SilphCo_9F_Text_Grunt2Intro, SilphCo_9F_Text_Grunt2Defeat
	msgbox SilphCo_9F_Text_Grunt2PostBattle, MSGBOX_AUTOCLOSE
	end

SilphCo_9F_OnTransition::
	goto_if_unset FLAG_HEMATEK_ALLIES_IN, SilphCo_9F_EventScript_HideAlly
	goto_if_set FLAG_HEMATEK_BOSS_DONE, SilphCo_9F_EventScript_HideAlly
	goto_if_set FLAG_HEMATEK_N_GONE, SilphCo_9F_EventScript_HideAlly
	end

SilphCo_9F_EventScript_HideAlly::
	setflag FLAG_TEMP_1
	end

SilphCo_9F_EventScript_Ally::
	lock
	faceplayer
	msgbox SilphCo_9F_Text_Ally
	closemessage
	applymovement LOCALID_SILPH_CO_9F_N, SilphCo_9F_Movement_AllyLeaves
	waitmovement 0
	removeobject LOCALID_SILPH_CO_9F_N
	setflag FLAG_HEMATEK_N_GONE
	release
	end

SilphCo_9F_Movement_AllyLeaves::
	walk_right
	walk_up
	walk_up
	step_end
