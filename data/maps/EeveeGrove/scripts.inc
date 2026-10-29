EeveeGrove_MapScripts::
	.byte 0

EeveeGrove_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EeveeGrove_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EeveeGrove_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EeveeGrove_EventScript_Stay::
	msgbox EeveeGrove_Text_Stay
	release
	end

EeveeGrove_EventScript_Npc0::
	msgbox EeveeGrove_Text_Npc0, MSGBOX_NPC
	end

EeveeGrove_EventScript_Npc1::
	msgbox EeveeGrove_Text_Npc1, MSGBOX_NPC
	end

EeveeGrove_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_EEVEEGROVE, EeveeGrove_EventScript_Quest0_After
	msgbox EeveeGrove_Text_Quest0_Ask
	checkitem ITEM_SODA_POP, 1
	goto_if_eq VAR_RESULT, FALSE, EeveeGrove_EventScript_Quest0_Miss
	checkitemspace ITEM_SOOTHE_BELL, 1
	goto_if_eq VAR_RESULT, FALSE, EeveeGrove_EventScript_Quest0_NoRoom
	removeitem ITEM_SODA_POP, 1
	giveitem ITEM_SOOTHE_BELL, 1
	setflag FLAG_TOPAZE_QUEST_EEVEEGROVE
	msgbox EeveeGrove_Text_Quest0_Done
	release
	end

EeveeGrove_EventScript_Quest0_After::
	msgbox EeveeGrove_Text_Quest0_AfterT
	release
	end

EeveeGrove_EventScript_Quest0_Miss::
	msgbox EeveeGrove_Text_Quest0_MissT
	release
	end

EeveeGrove_EventScript_Quest0_NoRoom::
	msgbox EeveeGrove_Text_Quest0_NoRoomT
	release
	end

