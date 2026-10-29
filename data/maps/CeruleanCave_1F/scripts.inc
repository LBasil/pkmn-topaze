CeruleanCave_1F_MapScripts::
	map_script MAP_SCRIPT_ON_TRANSITION, CeruleanCave_1F_OnTransition
	.byte 0

CeruleanCave_1F_OnTransition::
	setworldmapflag FLAG_WORLD_MAP_CERULEAN_CAVE_1F
	end

@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
CeruleanCave_1F_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_HID_CERULEANCAVE_1F_0, CeruleanCave_1F_EventScript_TopazeFind0_Done
	checkitemspace ITEM_MAX_REVIVE, 1
	goto_if_eq VAR_RESULT, FALSE, CeruleanCave_1F_EventScript_TopazeFind0_Full
	giveitem ITEM_MAX_REVIVE, 1
	setflag FLAG_TOPAZE_HID_CERULEANCAVE_1F_0
	release
	end

CeruleanCave_1F_EventScript_TopazeFind0_Done::
	release
	end

CeruleanCave_1F_EventScript_TopazeFind0_Full::
	msgbox CeruleanCave_1F_Text_TopazeFindFull
	release
	end

CeruleanCave_1F_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_HID_CERULEANCAVE_1F_1, CeruleanCave_1F_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, CeruleanCave_1F_EventScript_TopazeFind1_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_HID_CERULEANCAVE_1F_1
	release
	end

CeruleanCave_1F_EventScript_TopazeFind1_Done::
	release
	end

CeruleanCave_1F_EventScript_TopazeFind1_Full::
	msgbox CeruleanCave_1F_Text_TopazeFindFull
	release
	end


CeruleanCave_1F_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
