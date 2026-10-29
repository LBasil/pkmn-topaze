SeafoamIslands_B2F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeafoamIslands_B2F_OnTransition
	.byte 0

SeafoamIslands_B2F_OnTransition::
	call SeafoamIslands_B2F_EventScript_HideOnybris
	end

SeafoamIslands_B2F_EventScript_HideOnybris::
	goto_if_unset FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_B2F_EventScript_HideBeaten
	goto_if_set FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B2F_EventScript_HideBeaten
	return

SeafoamIslands_B2F_EventScript_HideBeaten::
	setflag FLAG_TEMP_6
	return

SeafoamIslands_B2F_EventScript_Onybris3::
	trainerbattle_single TRAINER_RS_GENTLEMAN, SeafoamIslands_B2F_Text_Onybris3Intro, SeafoamIslands_B2F_Text_Onybris3Defeat
	msgbox SeafoamIslands_B2F_Text_Onybris3Post, MSGBOX_AUTOCLOSE
	end

SeafoamIslands_B2F_EventScript_Onybris4::
	trainerbattle_single TRAINER_RS_BEAUTY, SeafoamIslands_B2F_Text_Onybris4Intro, SeafoamIslands_B2F_Text_Onybris4Defeat
	msgbox SeafoamIslands_B2F_Text_Onybris4Post, MSGBOX_AUTOCLOSE
	end

SeafoamIslands_B2F_EventScript_BeatenGrunt::
	msgbox SeafoamIslands_B2F_Text_BeatenGrunt, MSGBOX_NPC
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SeafoamIslands_B2F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_SEAFOAMISLANDS_B2F_0, SeafoamIslands_B2F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, SeafoamIslands_B2F_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_SEAFOAMISLANDS_B2F_0
	release
	end

SeafoamIslands_B2F_EventScript_TopazeFind0_Done::
	release
	end

SeafoamIslands_B2F_EventScript_TopazeFind0_Full::
	msgbox SeafoamIslands_B2F_Text_TopazeFindFull
	release
	end

SeafoamIslands_B2F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_SEAFOAMISLANDS_B2F_1, SeafoamIslands_B2F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, SeafoamIslands_B2F_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_SEAFOAMISLANDS_B2F_1
	release
	end

SeafoamIslands_B2F_EventScript_TopazeFind1_Done::
	release
	end

SeafoamIslands_B2F_EventScript_TopazeFind1_Full::
	msgbox SeafoamIslands_B2F_Text_TopazeFindFull
	release
	end


SeafoamIslands_B2F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
