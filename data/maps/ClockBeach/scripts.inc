ClockBeach_MapScripts::
	.byte 0

ClockBeach_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ClockBeach_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ClockBeach_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ClockBeach_EventScript_Stay::
	msgbox ClockBeach_Text_Stay
	release
	end

ClockBeach_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_BEACH, ClockBeach_EventScript_Boss_After
	msgbox ClockBeach_Text_Boss_Intro
	checkitemspace ITEM_RARE_CANDY, 3
	goto_if_eq VAR_RESULT, FALSE, ClockBeach_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_BEACH, ClockBeach_Text_Boss_Defeat
	giveitem ITEM_RARE_CANDY, 3
	msgbox ClockBeach_Text_Boss_After
	release
	end

ClockBeach_EventScript_Boss_After::
	msgbox ClockBeach_Text_Boss_After
	release
	end

ClockBeach_EventScript_Boss_NoRoom::
	msgbox ClockBeach_Text_Boss_NoRoom
	release
	end

ClockBeach_EventScript_Npc0::
	msgbox ClockBeach_Text_Npc0, MSGBOX_NPC
	end

ClockBeach_EventScript_Npc1::
	msgbox ClockBeach_Text_Npc1, MSGBOX_NPC
	end

