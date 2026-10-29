LastDayIsland_MapScripts::
	.byte 0

LastDayIsland_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox LastDayIsland_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, LastDayIsland_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

LastDayIsland_EventScript_Stay::
	msgbox LastDayIsland_Text_Stay
	release
	end

LastDayIsland_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_ISLAND, LastDayIsland_EventScript_Boss_After
	msgbox LastDayIsland_Text_Boss_Intro
	checkitemspace ITEM_RARE_CANDY, 10
	goto_if_eq VAR_RESULT, FALSE, LastDayIsland_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_ISLAND, LastDayIsland_Text_Boss_Defeat
	giveitem ITEM_RARE_CANDY, 10
	msgbox LastDayIsland_Text_Boss_After
	release
	end

LastDayIsland_EventScript_Boss_After::
	msgbox LastDayIsland_Text_Boss_After
	release
	end

LastDayIsland_EventScript_Boss_NoRoom::
	msgbox LastDayIsland_Text_Boss_NoRoom
	release
	end

LastDayIsland_EventScript_Npc0::
	msgbox LastDayIsland_Text_Npc0, MSGBOX_NPC
	end

