WhisperGrove_MapScripts::
	.byte 0

WhisperGrove_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox WhisperGrove_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, WhisperGrove_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

WhisperGrove_EventScript_Stay::
	msgbox WhisperGrove_Text_Stay
	release
	end

WhisperGrove_EventScript_Npc0::
	msgbox WhisperGrove_Text_Npc0, MSGBOX_NPC
	end

WhisperGrove_EventScript_Npc1::
	msgbox WhisperGrove_Text_Npc1, MSGBOX_NPC
	end

WhisperGrove_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_WHISPERGROVE, WhisperGrove_EventScript_Quest0_After
	msgbox WhisperGrove_Text_Quest0_Ask
	checkitem ITEM_NUGGET, 1
	goto_if_eq VAR_RESULT, FALSE, WhisperGrove_EventScript_Quest0_Miss
	checkitemspace ITEM_SPELL_TAG, 1
	goto_if_eq VAR_RESULT, FALSE, WhisperGrove_EventScript_Quest0_NoRoom
	removeitem ITEM_NUGGET, 1
	giveitem ITEM_SPELL_TAG, 1
	setflag FLAG_TOPAZE_QUEST_WHISPERGROVE
	msgbox WhisperGrove_Text_Quest0_Done
	release
	end

WhisperGrove_EventScript_Quest0_After::
	msgbox WhisperGrove_Text_Quest0_AfterT
	release
	end

WhisperGrove_EventScript_Quest0_Miss::
	msgbox WhisperGrove_Text_Quest0_MissT
	release
	end

WhisperGrove_EventScript_Quest0_NoRoom::
	msgbox WhisperGrove_Text_Quest0_NoRoomT
	release
	end

