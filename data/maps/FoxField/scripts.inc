FoxField_MapScripts::
	.byte 0

FoxField_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FoxField_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FoxField_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FoxField_EventScript_Stay::
	msgbox FoxField_Text_Stay
	release
	end

FoxField_EventScript_Npc0::
	msgbox FoxField_Text_Npc0, MSGBOX_NPC
	end

FoxField_EventScript_Npc1::
	msgbox FoxField_Text_Npc1, MSGBOX_NPC
	end

FoxField_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_FOXFIELD, FoxField_EventScript_Quest0_After
	msgbox FoxField_Text_Quest0_Ask
	checkitem ITEM_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, FoxField_EventScript_Quest0_Miss
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, FoxField_EventScript_Quest0_NoRoom
	removeitem ITEM_POTION, 2
	giveitem ITEM_CHARCOAL, 1
	setflag FLAG_TOPAZE_QUEST_FOXFIELD
	msgbox FoxField_Text_Quest0_Done
	release
	end

FoxField_EventScript_Quest0_After::
	msgbox FoxField_Text_Quest0_AfterT
	release
	end

FoxField_EventScript_Quest0_Miss::
	msgbox FoxField_Text_Quest0_MissT
	release
	end

FoxField_EventScript_Quest0_NoRoom::
	msgbox FoxField_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
FoxField_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FOXFIELD_0, FoxField_EventScript_TopazeFind0_Done
	checkitemspace ITEM_FIRE_STONE, 1
	goto_if_eq VAR_RESULT, FALSE, FoxField_EventScript_TopazeFind0_Full
	giveitem ITEM_FIRE_STONE, 1
	setflag FLAG_TOPAZE_FIND_FOXFIELD_0
	release
	end

FoxField_EventScript_TopazeFind0_Done::
	release
	end

FoxField_EventScript_TopazeFind0_Full::
	msgbox FoxField_Text_TopazeFindFull
	release
	end

FoxField_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FOXFIELD_1, FoxField_EventScript_TopazeFind1_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, FoxField_EventScript_TopazeFind1_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_FIND_FOXFIELD_1
	release
	end

FoxField_EventScript_TopazeFind1_Done::
	release
	end

FoxField_EventScript_TopazeFind1_Full::
	msgbox FoxField_Text_TopazeFindFull
	release
	end

FoxField_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FOXFIELD_2, FoxField_EventScript_TopazeFind2_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, FoxField_EventScript_TopazeFind2_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_FOXFIELD_2
	release
	end

FoxField_EventScript_TopazeFind2_Done::
	release
	end

FoxField_EventScript_TopazeFind2_Full::
	msgbox FoxField_Text_TopazeFindFull
	release
	end

