HushedBog_MapScripts::
	.byte 0

HushedBog_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox HushedBog_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, HushedBog_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

HushedBog_EventScript_Stay::
	msgbox HushedBog_Text_Stay
	release
	end

HushedBog_EventScript_Npc0::
	msgbox HushedBog_Text_Npc0, MSGBOX_NPC
	end

HushedBog_EventScript_Npc1::
	msgbox HushedBog_Text_Npc1, MSGBOX_NPC
	end

HushedBog_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_HUSHEDBOG, HushedBog_EventScript_Quest0_After
	msgbox HushedBog_Text_Quest0_Ask
	checkitem ITEM_FULL_HEAL, 1
	goto_if_eq VAR_RESULT, FALSE, HushedBog_EventScript_Quest0_Miss
	checkitemspace ITEM_POISON_BARB, 1
	goto_if_eq VAR_RESULT, FALSE, HushedBog_EventScript_Quest0_NoRoom
	removeitem ITEM_FULL_HEAL, 1
	giveitem ITEM_POISON_BARB, 1
	setflag FLAG_TOPAZE_QUEST_HUSHEDBOG
	msgbox HushedBog_Text_Quest0_Done
	release
	end

HushedBog_EventScript_Quest0_After::
	msgbox HushedBog_Text_Quest0_AfterT
	release
	end

HushedBog_EventScript_Quest0_Miss::
	msgbox HushedBog_Text_Quest0_MissT
	release
	end

HushedBog_EventScript_Quest0_NoRoom::
	msgbox HushedBog_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
HushedBog_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HUSHEDBOG_0, HushedBog_EventScript_TopazeFind0_Done
	checkitemspace ITEM_POISON_BARB, 1
	goto_if_eq VAR_RESULT, FALSE, HushedBog_EventScript_TopazeFind0_Full
	giveitem ITEM_POISON_BARB, 1
	setflag FLAG_TOPAZE_FIND_HUSHEDBOG_0
	release
	end

HushedBog_EventScript_TopazeFind0_Done::
	release
	end

HushedBog_EventScript_TopazeFind0_Full::
	msgbox HushedBog_Text_TopazeFindFull
	release
	end

HushedBog_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HUSHEDBOG_1, HushedBog_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, HushedBog_EventScript_TopazeFind1_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_HUSHEDBOG_1
	release
	end

HushedBog_EventScript_TopazeFind1_Done::
	release
	end

HushedBog_EventScript_TopazeFind1_Full::
	msgbox HushedBog_Text_TopazeFindFull
	release
	end

HushedBog_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_HUSHEDBOG_2, HushedBog_EventScript_TopazeFind2_Done
	checkitemspace ITEM_FULL_HEAL, 1
	goto_if_eq VAR_RESULT, FALSE, HushedBog_EventScript_TopazeFind2_Full
	giveitem ITEM_FULL_HEAL, 1
	setflag FLAG_TOPAZE_FIND_HUSHEDBOG_2
	release
	end

HushedBog_EventScript_TopazeFind2_Done::
	release
	end

HushedBog_EventScript_TopazeFind2_Full::
	msgbox HushedBog_Text_TopazeFindFull
	release
	end

