FangValley_MapScripts::
	.byte 0

FangValley_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox FangValley_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, FangValley_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

FangValley_EventScript_Stay::
	msgbox FangValley_Text_Stay
	release
	end

FangValley_EventScript_Npc0::
	msgbox FangValley_Text_Npc0, MSGBOX_NPC
	end

FangValley_EventScript_Npc1::
	msgbox FangValley_Text_Npc1, MSGBOX_NPC
	end

FangValley_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_FANGVALLEY, FangValley_EventScript_Quest0_After
	msgbox FangValley_Text_Quest0_Ask
	checkitem ITEM_FULL_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, FangValley_EventScript_Quest0_Miss
	checkitemspace ITEM_BLACK_GLASSES, 1
	goto_if_eq VAR_RESULT, FALSE, FangValley_EventScript_Quest0_NoRoom
	removeitem ITEM_FULL_HEAL, 2
	giveitem ITEM_BLACK_GLASSES, 1
	setflag FLAG_TOPAZE_QUEST_FANGVALLEY
	msgbox FangValley_Text_Quest0_Done
	release
	end

FangValley_EventScript_Quest0_After::
	msgbox FangValley_Text_Quest0_AfterT
	release
	end

FangValley_EventScript_Quest0_Miss::
	msgbox FangValley_Text_Quest0_MissT
	release
	end

FangValley_EventScript_Quest0_NoRoom::
	msgbox FangValley_Text_Quest0_NoRoomT
	release
	end


@ Topaze: objets caches (panneaux a script, drapeaux hors plage moteur)
FangValley_EventScript_TopazeFind0::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FANGVALLEY_0, FangValley_EventScript_TopazeFind0_Done
	checkitemspace ITEM_BLACK_GLASSES, 1
	goto_if_eq VAR_RESULT, FALSE, FangValley_EventScript_TopazeFind0_Full
	giveitem ITEM_BLACK_GLASSES, 1
	setflag FLAG_TOPAZE_FIND_FANGVALLEY_0
	release
	end

FangValley_EventScript_TopazeFind0_Done::
	release
	end

FangValley_EventScript_TopazeFind0_Full::
	msgbox FangValley_Text_TopazeFindFull
	release
	end

FangValley_EventScript_TopazeFind1::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FANGVALLEY_1, FangValley_EventScript_TopazeFind1_Done
	checkitemspace ITEM_MAX_POTION, 1
	goto_if_eq VAR_RESULT, FALSE, FangValley_EventScript_TopazeFind1_Full
	giveitem ITEM_MAX_POTION, 1
	setflag FLAG_TOPAZE_FIND_FANGVALLEY_1
	release
	end

FangValley_EventScript_TopazeFind1_Done::
	release
	end

FangValley_EventScript_TopazeFind1_Full::
	msgbox FangValley_Text_TopazeFindFull
	release
	end

FangValley_EventScript_TopazeFind2::
	lock
	goto_if_set FLAG_TOPAZE_FIND_FANGVALLEY_2, FangValley_EventScript_TopazeFind2_Done
	checkitemspace ITEM_FULL_HEAL, 1
	goto_if_eq VAR_RESULT, FALSE, FangValley_EventScript_TopazeFind2_Full
	giveitem ITEM_FULL_HEAL, 1
	setflag FLAG_TOPAZE_FIND_FANGVALLEY_2
	release
	end

FangValley_EventScript_TopazeFind2_Done::
	release
	end

FangValley_EventScript_TopazeFind2_Full::
	msgbox FangValley_Text_TopazeFindFull
	release
	end

