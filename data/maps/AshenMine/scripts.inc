AshenMine_MapScripts::
	.byte 0

AshenMine_EventScript_ReturnFerry::
	lock
	faceplayer
	msgbox AshenMine_Text_ReturnAsk, MSGBOX_YESNO
	goto_if_eq VAR_RESULT, NO, AshenMine_EventScript_Stay
	warp MAP_FUCHSIA_CITY, 255, 24, 27
	waitstate
	end

AshenMine_EventScript_Stay::
	msgbox AshenMine_Text_Stay
	release
	end

AshenMine_EventScript_Npc0::
	msgbox AshenMine_Text_Npc0, MSGBOX_NPC
	end

AshenMine_EventScript_Quest0::
	lock
	faceplayer
	goto_if_set FLAG_TOPAZE_QUEST_MINE, AshenMine_EventScript_Quest0_After
	msgbox AshenMine_Text_Quest0_Ask
	checkitem ITEM_STARDUST, 2
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_Quest0_Miss
	checkitemspace ITEM_DRAGON_SCALE, 1
	goto_if_eq VAR_RESULT, FALSE, AshenMine_EventScript_Quest0_NoRoom
	removeitem ITEM_STARDUST, 2
	giveitem ITEM_DRAGON_SCALE, 1
	setflag FLAG_TOPAZE_QUEST_MINE
	msgbox AshenMine_Text_Quest0_Done
	release
	end

AshenMine_EventScript_Quest0_After::
	msgbox AshenMine_Text_Quest0_AfterT
	release
	end

AshenMine_EventScript_Quest0_Miss::
	msgbox AshenMine_Text_Quest0_MissT
	release
	end

AshenMine_EventScript_Quest0_NoRoom::
	msgbox AshenMine_Text_Quest0_NoRoomT
	release
	end

