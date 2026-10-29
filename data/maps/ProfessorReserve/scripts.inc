ProfessorReserve_MapScripts::
	.byte 0

ProfessorReserve_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox ProfessorReserve_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, ProfessorReserve_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

ProfessorReserve_EventScript_Stay::
	msgbox ProfessorReserve_Text_Stay
	release
	end

ProfessorReserve_EventScript_Npc0::
	msgbox ProfessorReserve_Text_Npc0, MSGBOX_NPC
	end

ProfessorReserve_EventScript_Npc1::
	msgbox ProfessorReserve_Text_Npc1, MSGBOX_NPC
	end

ProfessorReserve_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_PROFESSORRESERVE, ProfessorReserve_EventScript_Quest0_After
	msgbox ProfessorReserve_Text_Quest0_Ask
	checkitem ITEM_RARE_CANDY, 1
	goto_if_eq VAR_RESULT, FALSE, ProfessorReserve_EventScript_Quest0_Miss
	checkitemspace ITEM_PP_MAX, 1
	goto_if_eq VAR_RESULT, FALSE, ProfessorReserve_EventScript_Quest0_NoRoom
	removeitem ITEM_RARE_CANDY, 1
	giveitem ITEM_PP_MAX, 1
	setflag FLAG_TOPAZE_QUEST_PROFESSORRESERVE
	msgbox ProfessorReserve_Text_Quest0_Done
	release
	end

ProfessorReserve_EventScript_Quest0_After::
	msgbox ProfessorReserve_Text_Quest0_AfterT
	release
	end

ProfessorReserve_EventScript_Quest0_Miss::
	msgbox ProfessorReserve_Text_Quest0_MissT
	release
	end

ProfessorReserve_EventScript_Quest0_NoRoom::
	msgbox ProfessorReserve_Text_Quest0_NoRoomT
	release
	end

