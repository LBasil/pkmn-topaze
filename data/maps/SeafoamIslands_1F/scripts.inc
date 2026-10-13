SeafoamIslands_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeafoamIslands_1F_OnTransition
	.byte 0

SeafoamIslands_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_SEAFOAM_ISLANDS_1F
	setflag FLAG_TEMP_1
	setflag FLAG_TEMP_2
	setflag FLAG_TEMP_3
	setflag FLAG_TEMP_4
	goto_if_set FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_1F_EventScript_AlliesDone
	end

SeafoamIslands_1F_EventScript_AlliesDone::
	setvar VAR_TEMP_1, 1
	end

SeafoamIslands_1F_EventScript_AllyStub::
	end

SeafoamIslands_1F_EventScript_AlliesWest::
	lockall
	clearflag FLAG_TEMP_1
	clearflag FLAG_TEMP_2
	addobject LOCALID_SEAFOAM_GOLD_W
	addobject LOCALID_SEAFOAM_SILVER_W
	playse SE_PIN
	delay 20
	applymovement LOCALID_SEAFOAM_GOLD_W, SeafoamIslands_1F_Movement_AllyDown
	applymovement LOCALID_SEAFOAM_SILVER_W, SeafoamIslands_1F_Movement_AllyDown
	waitmovement 0
	msgbox SeafoamIslands_1F_Text_GoldMeet
	msgbox SeafoamIslands_1F_Text_SilverMeet
	msgbox SeafoamIslands_1F_Text_GoldPlan
	msgbox SeafoamIslands_1F_Text_SilverPlan
	closemessage
	applymovement LOCALID_SEAFOAM_GOLD_W, SeafoamIslands_1F_Movement_AllyUp
	applymovement LOCALID_SEAFOAM_SILVER_W, SeafoamIslands_1F_Movement_AllyUp
	waitmovement 0
	removeobject LOCALID_SEAFOAM_GOLD_W
	removeobject LOCALID_SEAFOAM_SILVER_W
	setflag FLAG_SEAFOAM_ALLIES_MET
	setvar VAR_TEMP_1, 1
	releaseall
	end

SeafoamIslands_1F_EventScript_AlliesEast::
	lockall
	clearflag FLAG_TEMP_3
	clearflag FLAG_TEMP_4
	addobject LOCALID_SEAFOAM_GOLD_E
	addobject LOCALID_SEAFOAM_SILVER_E
	playse SE_PIN
	delay 20
	applymovement LOCALID_SEAFOAM_GOLD_E, SeafoamIslands_1F_Movement_AllyDown
	applymovement LOCALID_SEAFOAM_SILVER_E, SeafoamIslands_1F_Movement_AllyDown
	waitmovement 0
	msgbox SeafoamIslands_1F_Text_GoldMeet
	msgbox SeafoamIslands_1F_Text_SilverMeet
	msgbox SeafoamIslands_1F_Text_GoldPlan
	msgbox SeafoamIslands_1F_Text_SilverPlan
	closemessage
	applymovement LOCALID_SEAFOAM_GOLD_E, SeafoamIslands_1F_Movement_AllyUp
	applymovement LOCALID_SEAFOAM_SILVER_E, SeafoamIslands_1F_Movement_AllyUp
	waitmovement 0
	removeobject LOCALID_SEAFOAM_GOLD_E
	removeobject LOCALID_SEAFOAM_SILVER_E
	setflag FLAG_SEAFOAM_ALLIES_MET
	setvar VAR_TEMP_1, 1
	releaseall
	end

SeafoamIslands_1F_Movement_AllyDown::
	walk_down
	walk_down
	step_end

SeafoamIslands_1F_Movement_AllyUp::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	step_end
