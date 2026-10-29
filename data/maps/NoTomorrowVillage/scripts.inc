NoTomorrowVillage_MapScripts::
	.byte 0

NoTomorrowVillage_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox NoTomorrowVillage_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NoTomorrowVillage_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

NoTomorrowVillage_EventScript_Stay::
	msgbox NoTomorrowVillage_Text_Stay
	release
	end

NoTomorrowVillage_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_VILLAGE, NoTomorrowVillage_EventScript_Boss_After
	msgbox NoTomorrowVillage_Text_Boss_Intro
	checkitemspace ITEM_MAX_REVIVE, 3
	goto_if_eq VAR_RESULT, FALSE, NoTomorrowVillage_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_VILLAGE, NoTomorrowVillage_Text_Boss_Defeat
	giveitem ITEM_MAX_REVIVE, 3
	msgbox NoTomorrowVillage_Text_Boss_After
	release
	end

NoTomorrowVillage_EventScript_Boss_After::
	msgbox NoTomorrowVillage_Text_Boss_After
	release
	end

NoTomorrowVillage_EventScript_Boss_NoRoom::
	msgbox NoTomorrowVillage_Text_Boss_NoRoom
	release
	end

NoTomorrowVillage_EventScript_Npc0::
	goto_if_defeated TRAINER_ZONE_VILLAGE, NoTomorrowVillage_EventScript_Npc0_After
	msgbox NoTomorrowVillage_Text_Npc0, MSGBOX_NPC
	end

NoTomorrowVillage_EventScript_Npc0_After::
	msgbox NoTomorrowVillage_Text_Npc0_A, MSGBOX_NPC
	end

NoTomorrowVillage_EventScript_Npc1::
	goto_if_defeated TRAINER_ZONE_VILLAGE, NoTomorrowVillage_EventScript_Npc1_After
	msgbox NoTomorrowVillage_Text_Npc1, MSGBOX_NPC
	end

NoTomorrowVillage_EventScript_Npc1_After::
	msgbox NoTomorrowVillage_Text_Npc1_A, MSGBOX_NPC
	end

NoTomorrowVillage_EventScript_Npc2::
	goto_if_defeated TRAINER_ZONE_VILLAGE, NoTomorrowVillage_EventScript_Npc2_After
	msgbox NoTomorrowVillage_Text_Npc2, MSGBOX_NPC
	end

NoTomorrowVillage_EventScript_Npc2_After::
	msgbox NoTomorrowVillage_Text_Npc2_A, MSGBOX_NPC
	end

