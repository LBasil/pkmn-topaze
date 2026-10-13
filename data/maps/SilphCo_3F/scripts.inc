SilphCo_3F_MapScripts::
	map_script MAP_SCRIPT_ON_LOAD, SilphCo_3F_OnLoad
	map_script MAP_SCRIPT_ON_TRANSITION, SilphCo_3F_OnTransition
	.byte 0

SilphCo_3F_OnLoad::
	end

SilphCo_3F_EventScript_WorkerM::
	lock
	faceplayer
	goto_if_ge VAR_MAP_SCENE_SILPH_CO_11F, 1, SilphCo_3F_EventScript_WorkerMRocketsGone
	msgbox SilphCo_3F_Text_WhatAmIToDo
	release
	end

SilphCo_3F_EventScript_WorkerMRocketsGone::
	msgbox SilphCo_3F_Text_YouAndYourMonsSavedUs
	release
	end

SilphCo_3F_EventScript_FloorSign::
	msgbox SilphCo_3F_Text_FloorSign, MSGBOX_SIGN
	end

SilphCo_3F_EventScript_Jose::
	trainerbattle_single TRAINER_SCIENTIST_JOSE, SilphCo_3F_Text_JoseIntro, SilphCo_3F_Text_JoseDefeat
	msgbox SilphCo_3F_Text_JosePostBattle, MSGBOX_AUTOCLOSE
	end

SilphCo_3F_EventScript_Grunt::
	trainerbattle_single TRAINER_TEAM_ROCKET_GRUNT_25, SilphCo_3F_Text_GruntIntro, SilphCo_3F_Text_GruntDefeat
	msgbox SilphCo_3F_Text_GruntPostBattle, MSGBOX_AUTOCLOSE
	end

SilphCo_3F_OnTransition::
	goto_if_unset FLAG_HEMATEK_ALLIES_IN, SilphCo_3F_EventScript_HideAlly
	goto_if_set FLAG_HEMATEK_BOSS_DONE, SilphCo_3F_EventScript_HideAlly
	goto_if_set FLAG_HEMATEK_BRICE_GONE, SilphCo_3F_EventScript_HideAlly
	end

SilphCo_3F_EventScript_HideAlly::
	setflag FLAG_TEMP_1
	end

SilphCo_3F_EventScript_Ally::
	lock
	faceplayer
	msgbox SilphCo_3F_Text_Ally
	closemessage
	applymovement LOCALID_SILPH_CO_3F_BRICE, SilphCo_3F_Movement_AllyLeaves
	waitmovement 0
	removeobject LOCALID_SILPH_CO_3F_BRICE
	setflag FLAG_HEMATEK_BRICE_GONE
	release
	end

SilphCo_3F_Movement_AllyLeaves::
	walk_right
	walk_up
	walk_up
	step_end
