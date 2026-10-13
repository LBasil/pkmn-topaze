GrenaluxMine_3F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, GrenaluxMine_3F_OnTransition
	.byte 0

GrenaluxMine_3F_OnTransition::
	setflag FLAG_HIDE_MINE_MEW
	end

GrenaluxMine_3F_EventScript_ItemNugget::
	finditem ITEM_NUGGET
	end

@ Topaze: the truth about the AURA (placeholder text), then MEW appears and bolts.
GrenaluxMine_3F_EventScript_Truth::
	lockall
	goto_if_set FLAG_MEW_FLED, EventScript_ReleaseEnd
	msgbox GrenaluxMine_3F_Text_PendantGlows
	closemessage
	fadescreen FADE_TO_WHITE
	delay 30
	fadescreen FADE_FROM_WHITE
	msgbox GrenaluxMine_3F_Text_Vision1
	msgbox GrenaluxMine_3F_Text_Vision2
	msgbox GrenaluxMine_3F_Text_Vision3
	closemessage
	special ShakeScreen
	delay 30
	addobject LOCALID_MINE_MEW
	delay 20
	playmoncry SPECIES_MEW, CRY_MODE_NORMAL
	waitmoncry
	applymovement LOCALID_MINE_MEW, Common_Movement_WalkInPlaceFasterDown
	waitmovement 0
	msgbox GrenaluxMine_3F_Text_MewAppears
	closemessage
	applymovement LOCALID_MINE_MEW, GrenaluxMine_3F_Movement_MewFlees
	waitmovement 0
	removeobject LOCALID_MINE_MEW
	setflag FLAG_MEW_FLED
	msgbox GrenaluxMine_3F_Text_MewGone
	releaseall
	end

GrenaluxMine_3F_Movement_MewFlees::
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	walk_fast_up
	set_invisible
	step_end
