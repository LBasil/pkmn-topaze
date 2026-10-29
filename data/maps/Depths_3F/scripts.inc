Depths_3F_MapScripts::
	.byte 0

Depths_3F_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_CAVE, Depths_3F_EventScript_Boss_After
	msgbox Depths_3F_Text_Boss_Intro
	checkitemspace ITEM_RARE_CANDY, 5
	goto_if_eq VAR_RESULT, FALSE, Depths_3F_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_CAVE, Depths_3F_Text_Boss_Defeat
	giveitem ITEM_RARE_CANDY, 5
	msgbox Depths_3F_Text_Boss_After
	release
	end

Depths_3F_EventScript_Boss_After::
	msgbox Depths_3F_Text_Boss_After
	release
	end

Depths_3F_EventScript_Boss_NoRoom::
	msgbox Depths_3F_Text_Boss_NoRoom
	release
	end

Depths_3F_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox Depths_3F_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, Depths_3F_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

Depths_3F_EventScript_Stay::
	msgbox Depths_3F_Text_Stay
	release
	end
