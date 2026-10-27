SevenIsland_SevaultCanyon_Glade_MapScripts::
	map_script MAP_SCRIPT_ON_FRAME_TABLE, SevenIsland_SevaultCanyon_Glade_OnWarp
	.byte 0

SevenIsland_SevaultCanyon_Glade_OnWarp::
	map_script_2 VAR_TEMP_0, 0, SevenIsland_SevaultCanyon_Glade_Arrive
	.2byte 0

@ arrival on the exit-warp tile: step one tile inward (ON_FRAME, never ON_WARP: waitmovement hangs in an immediate script)
SevenIsland_SevaultCanyon_Glade_Arrive::
	setvar VAR_TEMP_0, 1
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
