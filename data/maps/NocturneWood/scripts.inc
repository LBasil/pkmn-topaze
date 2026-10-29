NocturneWood_MapScripts::
	.byte 0

NocturneWood_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox NocturneWood_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, NocturneWood_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

NocturneWood_EventScript_Stay::
	msgbox NocturneWood_Text_Stay
	release
	end

NocturneWood_EventScript_Npc0::
	msgbox NocturneWood_Text_Npc0, MSGBOX_NPC
	end

NocturneWood_EventScript_Npc1::
	msgbox NocturneWood_Text_Npc1, MSGBOX_NPC
	end

NocturneWood_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_NOCTURNEWOOD, NocturneWood_EventScript_Quest0_After
	msgbox NocturneWood_Text_Quest0_Ask
	checkitem ITEM_ANTIDOTE, 3
	goto_if_eq VAR_RESULT, FALSE, NocturneWood_EventScript_Quest0_Miss
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, NocturneWood_EventScript_Quest0_NoRoom
	removeitem ITEM_ANTIDOTE, 3
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_QUEST_NOCTURNEWOOD
	msgbox NocturneWood_Text_Quest0_Done
	release
	end

NocturneWood_EventScript_Quest0_After::
	msgbox NocturneWood_Text_Quest0_AfterT
	release
	end

NocturneWood_EventScript_Quest0_Miss::
	msgbox NocturneWood_Text_Quest0_MissT
	release
	end

NocturneWood_EventScript_Quest0_NoRoom::
	msgbox NocturneWood_Text_Quest0_NoRoomT
	release
	end

