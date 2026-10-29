HoneyGrove_MapScripts::
	.byte 0

HoneyGrove_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HoneyGrove_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HoneyGrove_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HoneyGrove_EventScript_Stay::
	msgbox HoneyGrove_Text_Stay
	release
	end

HoneyGrove_EventScript_Npc0::
	msgbox HoneyGrove_Text_Npc0, MSGBOX_NPC
	end

HoneyGrove_EventScript_Npc1::
	msgbox HoneyGrove_Text_Npc1, MSGBOX_NPC
	end

HoneyGrove_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_HONEYGROVE, HoneyGrove_EventScript_Quest0_After
	msgbox HoneyGrove_Text_Quest0_Ask
	checkitem ITEM_ANTIDOTE, 2
	goto_if_eq VAR_RESULT, FALSE, HoneyGrove_EventScript_Quest0_Miss
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, HoneyGrove_EventScript_Quest0_NoRoom
	removeitem ITEM_ANTIDOTE, 2
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_QUEST_HONEYGROVE
	msgbox HoneyGrove_Text_Quest0_Done
	release
	end

HoneyGrove_EventScript_Quest0_After::
	msgbox HoneyGrove_Text_Quest0_AfterT
	release
	end

HoneyGrove_EventScript_Quest0_Miss::
	msgbox HoneyGrove_Text_Quest0_MissT
	release
	end

HoneyGrove_EventScript_Quest0_NoRoom::
	msgbox HoneyGrove_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
HoneyGrove_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HONEYGROVE_0, HoneyGrove_EventScript_TopazeFind0_Done
	checkitemspace ITEM_SILVER_POWDER, 1
	goto_if_eq VAR_RESULT, FALSE, HoneyGrove_EventScript_TopazeFind0_Full
	giveitem ITEM_SILVER_POWDER, 1
	setflag FLAG_TOPAZE_FIND_HONEYGROVE_0
	release
	end

HoneyGrove_EventScript_TopazeFind0_Done::
	release
	end

HoneyGrove_EventScript_TopazeFind0_Full::
	msgbox HoneyGrove_Text_TopazeFindFull
	release
	end

HoneyGrove_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HONEYGROVE_1, HoneyGrove_EventScript_TopazeFind1_Done
	checkitemspace ITEM_SUPER_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, HoneyGrove_EventScript_TopazeFind1_Full
	giveitem ITEM_SUPER_POTION, 1
	setflag FLAG_TOPAZE_FIND_HONEYGROVE_1
	release
	end

HoneyGrove_EventScript_TopazeFind1_Done::
	release
	end

HoneyGrove_EventScript_TopazeFind1_Full::
	msgbox HoneyGrove_Text_TopazeFindFull
	release
	end

HoneyGrove_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HONEYGROVE_2, HoneyGrove_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, HoneyGrove_EventScript_TopazeFind2_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_HONEYGROVE_2
	release
	end

HoneyGrove_EventScript_TopazeFind2_Done::
	release
	end

HoneyGrove_EventScript_TopazeFind2_Full::
	msgbox HoneyGrove_Text_TopazeFindFull
	release
	end

