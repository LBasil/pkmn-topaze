OneIsland_Harbor_MapScripts::
	map_script MAP_SCRIPT_ON_WARP_INTO_MAP_TABLE, OneIsland_Harbor_OnWarp
	map_script MAP_SCRIPT_ON_FRAME_TABLE, OneIsland_Harbor_OnFrame
	.byte 0

OneIsland_Harbor_OnWarp::
	map_script_2 VAR_MAP_SCENE_ONE_ISLAND_HARBOR, 1, OneIsland_Harbor_EventScript_TurnPlayerNorth
	.2byte 0

OneIsland_Harbor_EventScript_TurnPlayerNorth::
	turnobject LOCALID_PLAYER, DIR_NORTH
	end

OneIsland_Harbor_OnFrame::
	map_script_2 VAR_MAP_SCENE_ONE_ISLAND_HARBOR, 1, OneIsland_Harbor_EventScript_PlayerEnterHarborFirstTime
	.2byte 0

OneIsland_Harbor_EventScript_PlayerEnterHarborFirstTime::
	lockall
	textcolor NPC_TEXT_COLOR_MALE
	applymovement LOCALID_PLAYER, OneIsland_Harbor_Movement_PlayerExitHarbor
	waitmovement 0
	setvar VAR_MAP_SCENE_ONE_ISLAND_HARBOR, 2
	warp MAP_ONE_ISLAND, 12, 18
	waitstate
	releaseall
	end

OneIsland_Harbor_Movement_PlayerExitHarbor::
	walk_up
	walk_up
	walk_up
	step_end

OneIsland_Harbor_EventScript_Sailor::
	lock
	faceplayer
	message Text_WhereDoYouWantToSail
	waitmessage
	setvar VAR_0x8004, SEAGALLOP_ONE_ISLAND
	goto EventScript_ChooseDestFromOneIsland
	end

@ Topaze: guide du port (post-game) : presente l'ile puis lit la boussole des Echos
OneIsland_Harbor_EventScript_Guide::
	lock
	faceplayer
	msgbox OneIsland_Harbor_Text_Guide
	goto_if_eq VAR_ECHO_STAGE, 0, OneIsland_Harbor_EventScript_GuideEnd
	msgbox OneIsland_Harbor_Text_GuideCompass
	closemessage
	goto EventScript_EchoCompass
	end

OneIsland_Harbor_EventScript_GuideEnd::
	release
	end

OneIsland_Harbor_Text_Guide::
	.string "Welcome to KINDLE ISLAND, the first\n"
	.string "stop of the SEVII ISLANDS.\l"
	.string "MT. EMBER keeps the island warm,\l"
	.string "and the PC here is a good base.\p"
	.string "Thunder never really stops here.\n"
	.string "RAIKOU runs the KINDLE ROAD, and\l"
	.string "MT. EMBER hides fire older still.\p"
	.string "You can sail to any island you\n"
	.string "like, in any order. Don't worry:\l"
	.string "I'll point you to the next ECHO.$"

OneIsland_Harbor_Text_GuideCompass::
	.string "Let me check the TIME COMPASS\n"
	.string "with you…$"
