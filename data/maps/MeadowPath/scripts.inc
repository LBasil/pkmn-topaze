MeadowPath_MapScripts::
	.byte 0

MeadowPath_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox MeadowPath_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, MeadowPath_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

MeadowPath_EventScript_Stay::
	msgbox MeadowPath_Text_Stay
	release
	end

MeadowPath_EventScript_Npc0::
	msgbox MeadowPath_Text_Npc0, MSGBOX_NPC
	end

MeadowPath_EventScript_Npc1::
	msgbox MeadowPath_Text_Npc1, MSGBOX_NPC
	end

MeadowPath_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MEADOWPATH, MeadowPath_EventScript_Quest0_After
	msgbox MeadowPath_Text_Quest0_Ask
	checkitem ITEM_POTION, 2
	goto_if_eq VAR_RESULT, FALSE, MeadowPath_EventScript_Quest0_Miss
	checkitemspace ITEM_EXP_SHARE, 1
	goto_if_eq VAR_RESULT, FALSE, MeadowPath_EventScript_Quest0_NoRoom
	removeitem ITEM_POTION, 2
	giveitem ITEM_EXP_SHARE, 1
	setflag FLAG_TOPAZE_QUEST_MEADOWPATH
	msgbox MeadowPath_Text_Quest0_Done
	release
	end

MeadowPath_EventScript_Quest0_After::
	msgbox MeadowPath_Text_Quest0_AfterT
	release
	end

MeadowPath_EventScript_Quest0_Miss::
	msgbox MeadowPath_Text_Quest0_MissT
	release
	end

MeadowPath_EventScript_Quest0_NoRoom::
	msgbox MeadowPath_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
MeadowPath_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MEADOWPATH_0, MeadowPath_EventScript_TopazeFind0_Done
	checkitemspace ITEM_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, MeadowPath_EventScript_TopazeFind0_Full
	giveitem ITEM_POTION, 1
	setflag FLAG_TOPAZE_FIND_MEADOWPATH_0
	release
	end

MeadowPath_EventScript_TopazeFind0_Done::
	release
	end

MeadowPath_EventScript_TopazeFind0_Full::
	msgbox MeadowPath_Text_TopazeFindFull
	release
	end

MeadowPath_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MEADOWPATH_1, MeadowPath_EventScript_TopazeFind1_Done
	checkitemspace ITEM_ANTIDOTE, 1
	goto_if_eq VAR_RESULT, FALSE, MeadowPath_EventScript_TopazeFind1_Full
	giveitem ITEM_ANTIDOTE, 1
	setflag FLAG_TOPAZE_FIND_MEADOWPATH_1
	release
	end

MeadowPath_EventScript_TopazeFind1_Done::
	release
	end

MeadowPath_EventScript_TopazeFind1_Full::
	msgbox MeadowPath_Text_TopazeFindFull
	release
	end

MeadowPath_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_MEADOWPATH_2, MeadowPath_EventScript_TopazeFind2_Done
	checkitemspace ITEM_POKE_BALL, 1
	goto_if_eq VAR_RESULT, FALSE, MeadowPath_EventScript_TopazeFind2_Full
	giveitem ITEM_POKE_BALL, 1
	setflag FLAG_TOPAZE_FIND_MEADOWPATH_2
	release
	end

MeadowPath_EventScript_TopazeFind2_Done::
	release
	end

MeadowPath_EventScript_TopazeFind2_Full::
	msgbox MeadowPath_Text_TopazeFindFull
	release
	end

