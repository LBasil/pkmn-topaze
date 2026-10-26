SevenIsland_SevaultCanyon_Glade_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, SevenIsland_SevaultCanyon_Glade_OnWarp
	.byte 0

SevenIsland_SevaultCanyon_Glade_OnWarp::
	map_script_2 VAR_TEMP_0, 0, SevenIsland_SevaultCanyon_Glade_Arrive
	.2byte 0

@ arrival on the exit-warp tile: step one tile inward so the player can walk back out (re-trigger the warp)
SevenIsland_SevaultCanyon_Glade_Arrive::
	getplayerxy VAR_0x8004, VAR_0x8005
	goto_if_ne VAR_0x8004, 7, SevenIsland_SevaultCanyon_Glade_ArriveEnd
	goto_if_eq VAR_0x8005, 13, SevenIsland_SevaultCanyon_Glade_StepUp
SevenIsland_SevaultCanyon_Glade_ArriveEnd::
	end

SevenIsland_SevaultCanyon_Glade_StepUp::
	applymovement OBJ_EVENT_ID_PLAYER, SevenIsland_SevaultCanyon_Glade_Movement_In
	waitmovement 0
	end

SevenIsland_SevaultCanyon_Glade_Movement_In::
	walk_up
	step_end
