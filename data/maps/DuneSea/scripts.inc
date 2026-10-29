DuneSea_MapScripts::
	.byte 0

DuneSea_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox DuneSea_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, DuneSea_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

DuneSea_EventScript_Stay::
	msgbox DuneSea_Text_Stay
	release
	end

DuneSea_EventScript_Npc0::
	msgbox DuneSea_Text_Npc0, MSGBOX_NPC
	end

DuneSea_EventScript_Npc1::
	msgbox DuneSea_Text_Npc1, MSGBOX_NPC
	end

DuneSea_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_DUNESEA, DuneSea_EventScript_Quest0_After
	msgbox DuneSea_Text_Quest0_Ask
	checkitem ITEM_FRESH_WATER, 2
	goto_if_eq VAR_RESULT, FALSE, DuneSea_EventScript_Quest0_Miss
	checkitemspace ITEM_SOFT_SAND, 1
	goto_if_eq VAR_RESULT, FALSE, DuneSea_EventScript_Quest0_NoRoom
	removeitem ITEM_FRESH_WATER, 2
	giveitem ITEM_SOFT_SAND, 1
	setflag FLAG_TOPAZE_QUEST_DUNESEA
	msgbox DuneSea_Text_Quest0_Done
	release
	end

DuneSea_EventScript_Quest0_After::
	msgbox DuneSea_Text_Quest0_AfterT
	release
	end

DuneSea_EventScript_Quest0_Miss::
	msgbox DuneSea_Text_Quest0_MissT
	release
	end

DuneSea_EventScript_Quest0_NoRoom::
	msgbox DuneSea_Text_Quest0_NoRoomT
	release
	end

