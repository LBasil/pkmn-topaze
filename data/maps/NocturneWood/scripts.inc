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


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
NocturneWood_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_NOCTURNEWOOD_0, NocturneWood_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, NocturneWood_EventScript_TopazeFind0_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_NOCTURNEWOOD_0
	release
	end

NocturneWood_EventScript_TopazeFind0_Done::
	release
	end

NocturneWood_EventScript_TopazeFind0_Full::
	msgbox NocturneWood_Text_TopazeFindFull
	release
	end

NocturneWood_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_NOCTURNEWOOD_1, NocturneWood_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, NocturneWood_EventScript_TopazeFind1_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_NOCTURNEWOOD_1
	release
	end

NocturneWood_EventScript_TopazeFind1_Done::
	release
	end

NocturneWood_EventScript_TopazeFind1_Full::
	msgbox NocturneWood_Text_TopazeFindFull
	release
	end

NocturneWood_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_NOCTURNEWOOD_2, NocturneWood_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ULTRA_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, NocturneWood_EventScript_TopazeFind2_Full
	giveitem ITEM_ULTRA_BALL, 1
	setflag FLAG_TOPAZE_FIND_NOCTURNEWOOD_2
	release
	end

NocturneWood_EventScript_TopazeFind2_Done::
	release
	end

NocturneWood_EventScript_TopazeFind2_Full::
	msgbox NocturneWood_Text_TopazeFindFull
	release
	end


NocturneWood_Text_TopazeFindFull::
	.string "Something shines here, but your BAG\n"
	.string "is full.$"
