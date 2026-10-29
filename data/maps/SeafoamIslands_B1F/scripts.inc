SeafoamIslands_B1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, SeafoamIslands_B1F_OnTransition
	.byte 0

SeafoamIslands_B1F_OnTransition::
	call SeafoamIslands_B1F_EventScript_HideOnybris
	end

SeafoamIslands_B1F_EventScript_HideOnybris::
	goto_if_unset FLAG_SEAFOAM_ALLIES_MET, SeafoamIslands_B1F_EventScript_HideBeaten
	goto_if_set FLAG_SEAFOAM_BOSS_DONE, SeafoamIslands_B1F_EventScript_HideBeaten
	return

SeafoamIslands_B1F_EventScript_HideBeaten::
	setflag FLAG_TEMP_6
	return

SeafoamIslands_B1F_EventScript_Onybris1::
	trainerbattle_single TRAINER_RS_TUBER_M, SeafoamIslands_B1F_Text_Onybris1Intro, SeafoamIslands_B1F_Text_Onybris1Defeat
	msgbox SeafoamIslands_B1F_Text_Onybris1Post, MSGBOX_AUTOCLOSE
	end

SeafoamIslands_B1F_EventScript_Onybris2::
	trainerbattle_single TRAINER_RS_TUBER_F, SeafoamIslands_B1F_Text_Onybris2Intro, SeafoamIslands_B1F_Text_Onybris2Defeat
	msgbox SeafoamIslands_B1F_Text_Onybris2Post, MSGBOX_AUTOCLOSE
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
SeafoamIslands_B1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_SEAFOAMISLANDS_B1F_0, SeafoamIslands_B1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_WATER_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, SeafoamIslands_B1F_EventScript_TopazeFind0_Full
	giveitem ITEM_WATER_STONE, 1
	setflag FLAG_TOPAZE_HID_SEAFOAMISLANDS_B1F_0
	release
	end

SeafoamIslands_B1F_EventScript_TopazeFind0_Done::
	release
	end

SeafoamIslands_B1F_EventScript_TopazeFind0_Full::
	msgbox SeafoamIslands_B1F_Text_TopazeFindFull
	release
	end

SeafoamIslands_B1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_SEAFOAMISLANDS_B1F_1, SeafoamIslands_B1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ELIXIR, 1
	goto_if_eq VAR_RESULT, FALSE, SeafoamIslands_B1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ELIXIR, 1
	setflag FLAG_TOPAZE_HID_SEAFOAMISLANDS_B1F_1
	release
	end

SeafoamIslands_B1F_EventScript_TopazeFind1_Done::
	release
	end

SeafoamIslands_B1F_EventScript_TopazeFind1_Full::
	msgbox SeafoamIslands_B1F_Text_TopazeFindFull
	release
	end


SeafoamIslands_B1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
