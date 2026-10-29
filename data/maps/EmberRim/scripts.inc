EmberRim_MapScripts::
	.byte 0

EmberRim_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox EmberRim_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, EmberRim_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

EmberRim_EventScript_Stay::
	msgbox EmberRim_Text_Stay
	release
	end

EmberRim_EventScript_Npc0::
	msgbox EmberRim_Text_Npc0, MSGBOX_NPC
	end

EmberRim_EventScript_Npc1::
	msgbox EmberRim_Text_Npc1, MSGBOX_NPC
	end

EmberRim_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_EMBERRIM, EmberRim_EventScript_Quest0_After
	msgbox EmberRim_Text_Quest0_Ask
	checkitem ITEM_ICE_HEAL, 2
	goto_if_eq VAR_RESULT, FALSE, EmberRim_EventScript_Quest0_Miss
	checkitemspace ITEM_CHARCOAL, 1
	goto_if_eq VAR_RESULT, FALSE, EmberRim_EventScript_Quest0_NoRoom
	removeitem ITEM_ICE_HEAL, 2
	giveitem ITEM_CHARCOAL, 1
	setflag FLAG_TOPAZE_QUEST_EMBERRIM
	msgbox EmberRim_Text_Quest0_Done
	release
	end

EmberRim_EventScript_Quest0_After::
	msgbox EmberRim_Text_Quest0_AfterT
	release
	end

EmberRim_EventScript_Quest0_Miss::
	msgbox EmberRim_Text_Quest0_MissT
	release
	end

EmberRim_EventScript_Quest0_NoRoom::
	msgbox EmberRim_Text_Quest0_NoRoomT
	release
	end

