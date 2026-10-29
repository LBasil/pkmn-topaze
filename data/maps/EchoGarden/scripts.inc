EchoGarden_MapScripts::
	.byte 0

EchoGarden_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EchoGarden_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EchoGarden_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EchoGarden_EventScript_Stay::
	msgbox EchoGarden_Text_Stay
	release
	end

EchoGarden_EventScript_Boss::
	lock
	faceplayer
	goto_if_defeated TRAINER_ZONE_GARDEN, EchoGarden_EventScript_Boss_After
	msgbox EchoGarden_Text_Boss_Intro
	checkitemspace ITEM_FULL_RESTORE, 3
	goto_if_eq VAR_RESULT, FALSE, EchoGarden_EventScript_Boss_NoRoom
	trainerbattle_no_intro TRAINER_ZONE_GARDEN, EchoGarden_Text_Boss_Defeat
	giveitem ITEM_FULL_RESTORE, 3
	msgbox EchoGarden_Text_Boss_After
	release
	end

EchoGarden_EventScript_Boss_After::
	msgbox EchoGarden_Text_Boss_After
	release
	end

EchoGarden_EventScript_Boss_NoRoom::
	msgbox EchoGarden_Text_Boss_NoRoom
	release
	end

EchoGarden_EventScript_Npc0::
	msgbox EchoGarden_Text_Npc0, MSGBOX_NPC
	end

EchoGarden_EventScript_Npc1::
	msgbox EchoGarden_Text_Npc1, MSGBOX_NPC
	end

