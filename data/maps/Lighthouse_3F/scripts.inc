Lighthouse_3F_MapScripts::
	.byte 0

Lighthouse_3F_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_LIGHTHOUSE, Lighthouse_3F_EventScript_Boss_After
	msgbox Lighthouse_3F_Text_Boss_Intro
	checkitemspace ITEM_PP_MAX, 2
	goto_if_eq VAR_RESULT, FALSE, Lighthouse_3F_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_LIGHTHOUSE, Lighthouse_3F_Text_Boss_Defeat
	giveitem ITEM_PP_MAX, 2
	msgbox Lighthouse_3F_Text_Boss_After
	release
	end

Lighthouse_3F_EventScript_Boss_After::
	msgbox Lighthouse_3F_Text_Boss_After
	release
	end

Lighthouse_3F_EventScript_Boss_NoRoom::
	msgbox Lighthouse_3F_Text_Boss_NoRoom
	release
	end

